from typing import Protocol
from uuid import UUID
from education_core.models import LabAttempt


class GetLabAttemptPort(Protocol):
    async def __call__(self, attempt_id: UUID) -> LabAttempt: ...
