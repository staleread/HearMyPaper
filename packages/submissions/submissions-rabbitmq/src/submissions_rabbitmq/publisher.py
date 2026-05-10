from typing import override
from shared_kernel.events import RabbitMQClient, SubmissionCommittedEvent
from submissions_core.ports.outgoing.event_publisher import EventPublisherPort


class RabbitMQEventPublisherAdapter(EventPublisherPort):
    def __init__(self, client: RabbitMQClient):
        self._client = client

    @override
    async def publish_submission_committed(
        self, event: SubmissionCommittedEvent
    ) -> None:
        await self._client.publish(routing_key="submission.committed", event=event)
