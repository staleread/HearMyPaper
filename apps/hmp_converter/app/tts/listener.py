import asyncio
import aio_pika
import json
from hmp_core.events import ConversionJobTask
from app.shared.dependencies.rabbitmq import get_event_client
from app.shared.dependencies.storage import get_storage_client
from . import service


async def process_task(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        task = None
        try:
            task = ConversionJobTask.model_validate_json(message.body)
            print(f" [x] Processing task: {task.job_id}")

            storage = get_storage_client()
            event_client = await get_event_client()

            await service.process_conversion(
                job_id=task.job_id,
                recipient_pseudonym=task.recipient_pseudonym,
                input_path=task.input_object_path,
                speed=task.speed,
                storage=storage,
                event_client=event_client,
            )

            print(f" [v] Completed task: {task.job_id}")
        except Exception as e:
            print(f" [!] Error processing task: {e}")
            if not task:
                return
            try:
                event_client = await get_event_client()
                error_code = "PROCESSING_FAILED"
                if "Decryption failed" in str(e):
                    error_code = "DECRYPTION_FAILED"
                elif "TTS" in str(e) or "Text-to-speech" in str(e):
                    error_code = "TTS_ENGINE_ERROR"

                failure_message = {
                    "conversion_uuid": str(task.job_id),
                    "status": "failed",
                    "error_code": error_code,
                    "error_message": str(e),
                }

                await event_client.declare_exchange("hmp.jobs.results")
                await event_client.publish(
                    routing_key="job.result.failure",
                    payload=json.dumps(failure_message).encode(),
                    correlation_id=str(task.job_id),
                )
            except Exception as pub_error:
                print(f" [!] Failed to publish error status: {pub_error}")


async def run_consumer():
    """Background task to run the RabbitMQ consumer."""
    try:
        client = await get_event_client()

        # Start consuming using the core client
        print(" [*] Consumer started. Waiting for messages.")
        await client.consume(
            queue_name="hmp.converter.v1.input",
            routing_key="job.request.pdf",
            callback=process_task,
            exchange_name="hmp.jobs.tts",
        )

        # Keep the background task alive
        await asyncio.Future()
    except asyncio.CancelledError:
        print(" [*] Consumer task cancelled.")
    except Exception as e:
        print(f" [!] Consumer error: {e}")
