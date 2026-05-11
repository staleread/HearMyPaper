from uuid import uuid4
from datetime import datetime, UTC
from ..models import Project
from ..exceptions import ProjectAlreadyExistsError, InstructorNotFoundError
from ..ports.incoming.create_project import (
    CreateProjectPort,
    CreateProjectCommand,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)
from ..ports.outgoing.identity_service import IdentityServicePort


class CreateProjectUseCase(CreateProjectPort):
    def __init__(self, projects: ProjectRepositoryPort, identity: IdentityServicePort):
        self._projects = projects
        self._identity = identity

    async def __call__(self, cmd: CreateProjectCommand) -> Project:
        if not await self._identity.verify_instructor_exists(cmd.instructor_id):
            raise InstructorNotFoundError(
                f"Instructor with ID '{cmd.instructor_id}' not found"
            )

        if await self._projects.exists_by_title(cmd.title):
            raise ProjectAlreadyExistsError(
                f"Project with title '{cmd.title}' already exists"
            )

        project = Project(
            id=uuid4(),
            title=cmd.title,
            description=cmd.description,
            instructor_id=cmd.instructor_id,
            deadline=cmd.deadline,
            created_at=datetime.now(UTC),
        )

        await self._projects.save(project)
        return project
