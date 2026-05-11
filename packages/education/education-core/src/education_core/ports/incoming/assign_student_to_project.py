from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AssignStudentToProjectCommand:
    project_id: UUID
    student_id: str


class AssignStudentToProjectPort(Protocol):
    async def __call__(self, cmd: AssignStudentToProjectCommand) -> None: ...
