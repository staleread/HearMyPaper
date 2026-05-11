from typing import Protocol
from uuid import UUID
from ...models import LabSubmission


class GetSubmissionPort(Protocol):
    async def __call__(self, submission_id: UUID) -> LabSubmission: ...
