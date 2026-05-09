from ..models import Project
from ..ports.incoming.get_user_projects import (
    GetUserProjectsPort,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class GetUserProjectsUseCase(GetUserProjectsPort):
    def __init__(self, projects: ProjectRepositoryPort):
        self._projects = projects

    async def __call__(self, user_id: str) -> list[Project]:
        return await self._projects.get_projects_by_user_id(user_id)
