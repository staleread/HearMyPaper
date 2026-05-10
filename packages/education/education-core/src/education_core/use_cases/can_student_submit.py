from uuid import UUID
from ..ports.incoming.can_student_submit import CanStudentSubmitPort
from ..ports.outgoing.project_repository import ProjectRepositoryPort
from ..ports.outgoing.project_student_repository import ProjectStudentRepositoryPort
from ..ports.outgoing.attempt_repository import AttemptRepositoryPort


class CanStudentSubmitUseCase(CanStudentSubmitPort):
    def __init__(
        self,
        projects: ProjectRepositoryPort,
        students: ProjectStudentRepositoryPort,
        attempts: AttemptRepositoryPort,
    ):
        self._projects = projects
        self._students = students
        self._attempts = attempts

    async def __call__(self, student_id: str, project_id: UUID) -> bool:
        project = await self._projects.get_by_id(project_id)
        if not project:
            return False

        # 1. Check if student is assigned to project
        if not await self._students.is_student_assigned(project_id, student_id):
            return False

        # 2. Check if an attempt already exists
        existing_attempt = await self._attempts.find_by_student_and_project(
            student_id, project_id
        )
        if existing_attempt:
            return False

        return True
