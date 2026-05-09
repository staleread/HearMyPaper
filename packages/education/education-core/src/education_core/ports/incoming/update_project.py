from dataclasses import dataclass
from typing import Protocol
from datetime import datetime
from uuid import UUID
from education_core.models import Project


@dataclass(frozen=True, slots=True)
class UpdateProjectCommand:
    title: str
    description: str
    deadline: datetime


class UpdateProjectPort(Protocol):
    async def __call__(
        self, project_id: UUID, cmd: UpdateProjectCommand
    ) -> Project: ...
