from dataclasses import dataclass
from typing import Protocol
from datetime import datetime
from education_core.models import Project


@dataclass(frozen=True, slots=True)
class CreateProjectCommand:
    title: str
    description: str
    instructor_id: str
    deadline: datetime


class CreateProjectPort(Protocol):
    async def __call__(self, cmd: CreateProjectCommand) -> Project: ...
