from hmp_manager.education.domain.exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    StudentAlreadyAssignedError,
)
from hmp_manager.education.domain.ports.incoming.assign_student_to_project import (
    AssignStudentToProjectPort,
    AssignStudentToProjectCommand,
)
from hmp_manager.education.domain.ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)
from hmp_manager.education.domain.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)
from hmp_manager.education.domain.ports.outgoing.identity_service import (
    IdentityServicePort,
)


class AssignStudentToProjectUseCase(AssignStudentToProjectPort):
    def __init__(
        self,
        projects: ProjectRepositoryPort,
        project_students: ProjectStudentRepositoryPort,
        identity: IdentityServicePort,
    ):
        self._projects = projects
        self._project_students = project_students
        self._identity = identity

    async def __call__(self, cmd: AssignStudentToProjectCommand) -> None:
        # Verify project exists
        project = await self._projects.get_by_id(cmd.project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {cmd.project_id} not found")

        # Verify student exists in identity
        if not await self._identity.verify_student_exists(cmd.student_id):
            raise StudentNotFoundError(f"Student with id {cmd.student_id} not found")

        # Check if already assigned
        if await self._project_students.is_student_assigned(
            cmd.project_id, cmd.student_id
        ):
            raise StudentAlreadyAssignedError(
                f"Student {cmd.student_id} is already assigned to project {cmd.project_id}"
            )

        await self._project_students.add_student(cmd.project_id, cmd.student_id)
