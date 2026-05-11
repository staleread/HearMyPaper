from typing import Protocol
from uuid import UUID


class GradeAttemptPort(Protocol):
    async def __call__(
        self, attempt_id: UUID, grade: int, feedback: str | None
    ) -> None: ...
