from typing import Protocol
from uuid import UUID
from ...models import LabAttempt


class GetProjectAttemptsPort(Protocol):
    async def __call__(self, project_id: UUID) -> list[LabAttempt]: ...
