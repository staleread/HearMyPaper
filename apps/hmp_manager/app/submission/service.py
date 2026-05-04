from hmp_core.events.models import ConversionJobTask
from app.shared.dependencies.rabbitmq import get_event_client

async def publish_conversion_task(task: ConversionJobTask) -> None:
    """
    Publishes a validated conversion task to RabbitMQ.
    Routing Key: job.request.pdf
    """
    client = await get_event_client()
    
    await client.publish(
        routing_key="job.request.pdf",
        payload=task.model_dump_json().encode(),
        correlation_id=task.correlation_id,
    )
