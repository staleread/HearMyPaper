from uuid import uuid4
from datetime import datetime, UTC
from ..models import Project
from ..exceptions import ProjectAlreadyExistsError
from ..ports.incoming.create_project import (
    CreateProjectPort,
    CreateProjectCommand,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class CreateProjectUseCase(CreateProjectPort):
    def __init__(self, projects: ProjectRepositoryPort):
        self._projects = projects

    async def __call__(self, cmd: CreateProjectCommand) -> Project:
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
