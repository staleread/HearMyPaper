from ..exceptions import (
    ProjectNotFoundError,
    StudentNotAssignedError,
)
from ..ports.incoming.remove_student_from_project import (
    RemoveStudentFromProjectPort,
    RemoveStudentFromProjectCommand,
)
from ..ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)
from ..ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)


class RemoveStudentFromProjectUseCase(RemoveStudentFromProjectPort):
    def __init__(
        self,
        projects: ProjectRepositoryPort,
        project_students: ProjectStudentRepositoryPort,
    ):
        self._projects = projects
        self._project_students = project_students

    async def __call__(self, cmd: RemoveStudentFromProjectCommand) -> None:
        # Verify project exists
        project = await self._projects.get_by_id(cmd.project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {cmd.project_id} not found")

        # Check if assigned
        if not await self._project_students.is_student_assigned(
            cmd.project_id, cmd.student_id
        ):
            raise StudentNotAssignedError(
                f"Student {cmd.student_id} is not assigned to project {cmd.project_id}"
            )

        await self._project_students.remove_student(cmd.project_id, cmd.student_id)
