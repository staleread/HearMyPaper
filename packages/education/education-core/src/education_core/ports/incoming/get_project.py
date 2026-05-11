from typing import Protocol
from uuid import UUID
from education_core.models import Project


class GetProjectPort(Protocol):
    async def __call__(self, project_id: UUID) -> Project: ...
