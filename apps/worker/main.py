import asyncio
import json
import uuid
import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict
from shared_kernel.events import RabbitMQClient, TaskStatusUpdatedEvent
from shared_kernel.crypto import generate_keypair
from shared_kernel.marshal import to_b64


class WorkerSettings(BaseSettings):
    worker_id: uuid.UUID = uuid.uuid4()
    leader_url: str = "http://localhost:8000"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    heartbeat_interval: int = 20
    capabilities: list[str] = ["pdf-to-audio"]

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
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    print("[INFO] Heartbeat sent")
                else:
                    print(f"[WARN] Heartbeat failed with status {resp.status_code}")
            except Exception as e:
                print(f"[ERROR] Heartbeat failed: {e}")

            await asyncio.sleep(settings.heartbeat_interval)


class WorkerCoordinator:
    def __init__(self, rabbit_client: RabbitMQClient, private_key: bytes):
        self._rabbit_client = rabbit_client
        self._private_key = private_key

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

                    print(f"[INFO] Received task {task_id}")

                    await self._report_status(task_id, "processing")

                    # Execute (Milestone 3 placeholder)
                    await asyncio.sleep(5)  # Simulate work

                    await self._report_status(task_id, "completed")
                    print(f"[INFO] Task {task_id} completed")

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
    coordinator = WorkerCoordinator(rabbit_client, private_key)

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
