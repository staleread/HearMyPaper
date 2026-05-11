from typing import Protocol
from uuid import UUID
from ...models import LabAttempt


class GetAttemptPort(Protocol):
    async def __call__(self, attempt_id: UUID) -> LabAttempt | None: ...
