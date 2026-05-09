from typing import Protocol
from uuid import UUID
from education_core.models import Project


class ProjectRepositoryPort(Protocol):
    async def get_projects_by_user_id(self, user_id: str) -> list[Project]: ...
    async def get_by_id(self, project_id: UUID) -> Project | None: ...
