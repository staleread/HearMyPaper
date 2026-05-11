from dataclasses import replace
from uuid import UUID
from ..models import Project
from ..exceptions import (
    ProjectNotFoundError,
    ProjectAlreadyExistsError,
    InstructorNotFoundError,
)
from ..ports.incoming.update_project import (
    UpdateProjectPort,
    UpdateProjectCommand,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)
from ..ports.outgoing.identity_service import IdentityServicePort


class UpdateProjectUseCase(UpdateProjectPort):
    def __init__(self, projects: ProjectRepositoryPort, identity: IdentityServicePort):
        self._projects = projects
        self._identity = identity

    async def __call__(self, project_id: UUID, cmd: UpdateProjectCommand) -> Project:
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        if not await self._identity.verify_instructor_exists(cmd.instructor_id):
            raise InstructorNotFoundError(
                f"Instructor with ID '{cmd.instructor_id}' not found"
            )

        if cmd.title != project.title:
            if await self._projects.exists_by_title(cmd.title):
                raise ProjectAlreadyExistsError(
                    f"Project with title '{cmd.title}' already exists"
                )

        updated_project = replace(
            project,
            title=cmd.title,
            description=cmd.description,
            instructor_id=cmd.instructor_id,
            deadline=cmd.deadline,
        )

        await self._projects.update(updated_project)
        return updated_project
