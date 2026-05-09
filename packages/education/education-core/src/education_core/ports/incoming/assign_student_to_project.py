from typing import Protocol
from uuid import UUID
from pydantic import BaseModel


class AssignStudentToProjectCommand(BaseModel):
    project_id: UUID
    student_id: str


class AssignStudentToProjectPort(Protocol):
    async def __call__(self, cmd: AssignStudentToProjectCommand) -> None: ...
