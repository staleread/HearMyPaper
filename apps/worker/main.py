import asyncio
import json
import uuid
import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared_kernel.events import RabbitMQClient, TaskStatusUpdatedEvent
from shared_kernel.crypto import generate_keypair, unseal, seal
from shared_kernel.marshal import to_b64, from_b64

from processing_parser import PyMuPDFParserAdapter
from processing_tts import ESpeakTTSAdapter


class WorkerSettings(BaseSettings):
    worker_id: uuid.UUID = uuid.uuid4()
    leader_url: str = "http://localhost:8000"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    heartbeat_interval: int = 20
    capabilities: list[str] = ["pdf_to_audio"]

    model_config = SettingsConfigDict(env_prefix="WORKER_")


settings = WorkerSettings()


async def register_worker(public_key: bytes):
    """Initial registration with the Leader."""
    url = f"{settings.leader_url}/orchestrator/workers/register"
    payload = {
        "worker_id": str(settings.worker_id),
        "public_key_b64": to_b64(public_key),
        "capabilities": settings.capabilities,
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                print("[INFO] Worker registered successfully")
                return True
            else:
                print(f"[ERROR] Registration failed with status {resp.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            return False


async def send_heartbeat():
    """Background task to send periodic liveness heartbeats."""
    url = f"{settings.leader_url}/orchestrator/workers/heartbeat"
    payload = {
        "worker_id": str(settings.worker_id),
    }

    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.post(url, json=payload, timeout=5.0)
                if resp.status_code == 200:
                    print("[INFO] Heartbeat sent")
                else:
                    print(f"[WARN] Heartbeat failed with status {resp.status_code}")
            except Exception as e:
                print(f"[ERROR] Heartbeat failed: {e}")

            await asyncio.sleep(settings.heartbeat_interval)


class WorkerCoordinator:
    def __init__(
        self,
        rabbit_client: RabbitMQClient,
        private_key: bytes,
        parser: PyMuPDFParserAdapter,
        tts: ESpeakTTSAdapter,
    ):
        self._rabbit_client = rabbit_client
        self._private_key = private_key
        self._parser = parser
        self._tts = tts

    async def start_listening(self):
        """Listen for tasks assigned specifically to this worker."""
        await self._rabbit_client.connect()
        channel = self._rabbit_client.channel
        exchange = self._rabbit_client.exchange

        # Exclusive queue for this worker's tasks
        queue_name = f"worker.{settings.worker_id}.tasks"
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        await queue.bind(exchange, routing_key=f"worker.{settings.worker_id}.tasks")

        print(f"[INFO] Worker listening on {queue_name}")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    task_id = uuid.UUID(payload["task_id"])
                    source_url = payload["source_download_url"]
                    result_url = payload["result_upload_url"]
                    sealing_key_b64 = payload["sealing_key_b64"]

                    print(f"[INFO] Received task {task_id}")

                    try:
                        # 1. Notify: Processing
                        await self._report_status(task_id, "processing")

                        # 2. Download source
                        print(f"[INFO] Downloading source for task {task_id}")
                        async with httpx.AsyncClient() as http:
                            resp = await http.get(source_url)
                            resp.raise_for_status()
                            sealed_pdf = resp.content

                        # 3. Unseal
                        print(f"[INFO] Unsealing PDF for task {task_id}")
                        pdf_bytes = unseal(
                            sealed_pdf, private_key_bytes=self._private_key
                        )

                        # 4. Extract Text
                        print(f"[INFO] Extracting text for task {task_id}")
                        text = await self._parser.extract_text(pdf_bytes)
                        if not text.strip():
                            raise ValueError("PDF contains no text")

                        # 5. TTS
                        print(f"[INFO] Converting to speech for task {task_id}")
                        audio_bytes = await self._tts.text_to_speech(text)

                        # 6. Seal Audio
                        print(f"[INFO] Sealing audio for task {task_id}")
                        sealed_audio = seal(
                            audio_bytes, public_key_bytes=from_b64(sealing_key_b64)
                        )

                        # 7. Upload result
                        print(f"[INFO] Uploading result for task {task_id}")
                        async with httpx.AsyncClient() as http:
                            resp = await http.put(
                                result_url,
                                content=sealed_audio,
                                headers={"Content-Type": "application/octet-stream"},
                            )
                            resp.raise_for_status()

                        # 8. Notify: Completed
                        await self._report_status(task_id, "completed")
                        print(f"[INFO] Task {task_id} completed successfully")

                    except Exception as e:
                        print(f"[ERROR] Task {task_id} failed: {e}")
                        await self._report_status(task_id, "failed")

    async def _report_status(self, task_id: uuid.UUID, status: str):
        event = TaskStatusUpdatedEvent(task_id=task_id, status=status)
        await self._rabbit_client.publish("task.status.updated", event)


async def main():
    private_key, public_key = generate_keypair()
    print(f"[INFO] Generated transient keypair for worker {settings.worker_id}")

    # 1. Register first
    if not await register_worker(public_key):
        print("[CRITICAL] Could not register worker. Exiting.")
        return

    rabbit_client = RabbitMQClient(settings.rabbitmq_url)

    # Initialize Adapters
    parser = PyMuPDFParserAdapter()
    tts = ESpeakTTSAdapter()

    coordinator = WorkerCoordinator(rabbit_client, private_key, parser, tts)

    # 2. Run listener and heartbeat concurrently
    try:
        await asyncio.gather(
            coordinator.start_listening(),
            send_heartbeat(),
        )
    except asyncio.CancelledError:
        print("[INFO] Worker shutting down...")
    finally:
        await rabbit_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
