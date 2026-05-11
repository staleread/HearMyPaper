from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RemoveStudentFromProjectCommand:
    project_id: UUID
    student_id: str


class RemoveStudentFromProjectPort(Protocol):
    async def __call__(self, cmd: RemoveStudentFromProjectCommand) -> None: ...
