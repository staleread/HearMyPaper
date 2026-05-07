from hmp_manager.education.domain.models import Project
from hmp_manager.education.domain.ports.incoming.get_user_projects import (
    GetUserProjectsPort,
)
from hmp_manager.education.domain.ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class GetUserProjectsUseCase(GetUserProjectsPort):
    def __init__(self, projects: ProjectRepositoryPort):
        self._projects = projects

    async def __call__(self, user_id: str) -> list[Project]:
        return await self._projects.get_projects_by_user_id(user_id)
