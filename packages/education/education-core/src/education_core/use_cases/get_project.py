from uuid import UUID
from ..models import Project
from ..exceptions import ProjectNotFoundError
from ..ports.incoming.get_project import GetProjectPort
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class GetProjectUseCase(GetProjectPort):
    def __init__(self, projects: ProjectRepositoryPort):
        self._projects = projects

    async def __call__(self, project_id: UUID) -> Project:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {project_id} not found")
        return project
