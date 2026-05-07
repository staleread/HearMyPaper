from uuid import UUID
from hmp_manager.education.domain.exceptions import ProjectNotFoundError
from hmp_manager.education.domain.ports.incoming.get_project_students import (
    GetProjectStudentsPort,
)
from hmp_manager.education.domain.ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)
from hmp_manager.education.domain.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)


class GetProjectStudentsUseCase(GetProjectStudentsPort):
    def __init__(
        self,
        projects: ProjectRepositoryPort,
        project_students: ProjectStudentRepositoryPort,
    ):
        self._projects = projects
        self._project_students = project_students

    async def __call__(self, project_id: UUID) -> list[str]:
        # Verify project exists
        project = await self._projects.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {project_id} not found")

        return await self._project_students.get_student_ids(project_id)
