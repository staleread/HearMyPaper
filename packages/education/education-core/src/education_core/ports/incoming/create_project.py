from typing import Protocol
from datetime import datetime
from pydantic import BaseModel
from education_core.models import Project


class CreateProjectCommand(BaseModel):
    title: str
    description: str
    instructor_id: str
    deadline: datetime


class CreateProjectPort(Protocol):
    async def __call__(self, cmd: CreateProjectCommand) -> Project: ...
