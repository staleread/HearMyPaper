from uuid import UUID
from ..models import Project
from ..exceptions import ProjectNotFoundError, ProjectAlreadyExistsError
from ..ports.incoming.update_project import (
    UpdateProjectPort,
    UpdateProjectCommand,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class UpdateProjectUseCase(UpdateProjectPort):
    def __init__(self, projects: ProjectRepositoryPort):
        self._projects = projects

    async def __call__(self, project_id: UUID, cmd: UpdateProjectCommand) -> Project:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        if cmd.title != project.title:
            if await self._projects.exists_by_title(cmd.title):
                raise ProjectAlreadyExistsError(
                    f"Project with title '{cmd.title}' already exists"
                )

        project.title = cmd.title
        project.description = cmd.description
        project.deadline = cmd.deadline

        await self._projects.update(project)
        return project
