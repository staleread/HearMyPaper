from typing import Protocol
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterAttemptCommand:
    submission_id: UUID
    student_id: str
    project_id: UUID
    timestamp: datetime


class RegisterAttemptPort(Protocol):
    async def __call__(self, cmd: RegisterAttemptCommand) -> None:
        """Registers a new lab attempt based on a submission."""
        ...
