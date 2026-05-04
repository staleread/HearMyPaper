import asyncio
import aio_pika
from hmp_core.events.models import ConversionJobTask
from app.shared.dependencies.rabbitmq import get_event_client

async def process_task(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            task = ConversionJobTask.model_validate_json(message.body)
            print(f" [x] Processing task: {task.job_id}")
            
            # TODO: Full implementation (MinIO, Decryption, etc.)
            
            print(f" [v] Completed task: {task.job_id}")
        except Exception as e:
            print(f" [!] Error processing task: {e}")

async def run_consumer():
    """Background task to run the RabbitMQ consumer."""
    try:
        client = await get_event_client()
        
        # Start consuming using the core client
        print(" [*] Consumer started. Waiting for messages.")
        await client.consume(
            queue_name="hmp.converter.v1.input",
            routing_key="job.request.pdf",
            callback=process_task
        )
        
        # Keep the background task alive
        await asyncio.Future()
    except asyncio.CancelledError:
        print(" [*] Consumer task cancelled.")
    except Exception as e:
        print(f" [!] Consumer error: {e}")
