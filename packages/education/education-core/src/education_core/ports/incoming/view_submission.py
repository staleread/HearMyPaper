from typing import Protocol
from uuid import UUID


class ViewSubmissionPort(Protocol):
    async def __call__(self, instructor_id: str, submission_id: UUID) -> str:
        """Returns a download URL for the given submission, verifying instructor access."""
        ...
