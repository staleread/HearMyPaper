from typing import override
from uuid import UUID
from orchestrator_core.ports.outgoing.event_publisher import EventPublisherPort
from shared_kernel.events import RabbitMQClient, TaskDispatchedEvent
from shared_kernel.marshal import to_b64


class RabbitMQEventPublisherAdapter(EventPublisherPort):
    def __init__(self, rabbit_client: RabbitMQClient):
        self._rabbit_client = rabbit_client

    @override
    async def publish_task_dispatched(
        self,
        worker_id: UUID,
        task_id: UUID,
        task_type: str,
        source_download_url: str,
        result_upload_url: str,
        sealing_key: bytes,
    ) -> None:
        event = TaskDispatchedEvent(
            task_id=task_id,
            task_type=task_type,
            source_download_url=source_download_url,
            result_upload_url=result_upload_url,
            sealing_key_b64=to_b64(sealing_key),
        )

        routing_key = f"worker.{worker_id}.tasks"
        await self._rabbit_client.publish(routing_key, event)
