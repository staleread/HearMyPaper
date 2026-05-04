import asyncio
import aio_pika
import json
from uuid import UUID
from app.shared.dependencies.rabbitmq import get_event_client
from app.shared.dependencies.db import get_db_runner_context
from . import repository


async def process_result(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body)
            conversion_uuid = UUID(payload["conversion_uuid"])
            status = payload["status"]
            error_message = payload.get("error_message")
            output_path = payload.get("output_path")

            print(f" [x] Updating conversion {conversion_uuid} to {status}")

            async with get_db_runner_context() as db:
                repository.update_conversion_status(
                    conversion_uuid=conversion_uuid,
                    status=status,
                    db=db,
                    error_message=error_message,
                    output_path=output_path,
                )

            print(f" [v] Updated conversion {conversion_uuid}")
        except Exception as e:
            print(f" [!] Error processing result message: {e}")


async def run_result_consumer():
    """Background task to run the RabbitMQ consumer for results."""
    try:
        client = await get_event_client()

        print(" [*] Result consumer started. Waiting for messages.")
        await client.consume(
            queue_name="hmp.manager.v1.results",
            routing_key="job.result.#",  # Listen for both success and failure
            callback=process_result,
            exchange_name="hmp.jobs.results",
        )

        await asyncio.Future()
    except asyncio.CancelledError:
        print(" [*] Result consumer task cancelled.")
    except Exception as e:
        print(f" [!] Result consumer error: {e}")
