from typing import Protocol
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from education_core.models import Project


class UpdateProjectCommand(BaseModel):
    title: str
    description: str
    deadline: datetime


class UpdateProjectPort(Protocol):
    async def __call__(
        self, project_id: UUID, cmd: UpdateProjectCommand
    ) -> Project: ...
