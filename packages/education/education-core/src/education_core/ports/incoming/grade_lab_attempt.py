from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GradeLabAttemptCommand:
    attempt_id: UUID
    instructor_id: str
    grade: int
    feedback: str | None = None


class GradeLabAttemptPort(Protocol):
    async def __call__(self, cmd: GradeLabAttemptCommand) -> None:
        """Grades a lab attempt, providing feedback and a score."""
        ...
