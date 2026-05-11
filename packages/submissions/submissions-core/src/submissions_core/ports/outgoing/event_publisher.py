from typing import Protocol
from shared_kernel.events import SubmissionCommittedEvent


class EventPublisherPort(Protocol):
    async def publish_submission_committed(
        self, event: SubmissionCommittedEvent
    ) -> None:
        """Publishes the SubmissionCommittedEvent to the message broker."""
        ...
