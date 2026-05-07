from typing import Protocol
from uuid import UUID
from pydantic import BaseModel


class RemoveStudentFromProjectCommand(BaseModel):
    project_id: UUID
    student_id: str


class RemoveStudentFromProjectPort(Protocol):
    async def __call__(self, cmd: RemoveStudentFromProjectCommand) -> None: ...
