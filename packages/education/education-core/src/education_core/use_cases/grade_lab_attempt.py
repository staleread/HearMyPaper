from ..ports.incoming.grade_lab_attempt import (
    GradeLabAttemptPort,
    GradeLabAttemptCommand,
)
from ..ports.outgoing.attempt_repository import AttemptRepositoryPort
from ..ports.outgoing.project_repository import ProjectRepositoryPort
from ..exceptions import (
    AccessDeniedError,
    AttemptNotFoundError,
    ProjectNotFoundError,
    AttemptAlreadyGradedError,
    InvalidGradeError,
)


class GradeLabAttemptUseCase(GradeLabAttemptPort):
    def __init__(
        self,
        attempts: AttemptRepositoryPort,
        projects: ProjectRepositoryPort,
    ):
        self._attempts = attempts
        self._projects = projects

    async def __call__(self, cmd: GradeLabAttemptCommand) -> None:
        attempt = await self._attempts.get_by_id(cmd.attempt_id)
        if not attempt:
            raise AttemptNotFoundError(f"Attempt {cmd.attempt_id} not found")

        if attempt.grade is not None:
            raise AttemptAlreadyGradedError(
                f"Attempt {cmd.attempt_id} is already graded"
            )

        project = await self._projects.get_by_id(attempt.project_id)
        if not project:
            raise ProjectNotFoundError(f"Project {attempt.project_id} not found")

        if project.instructor_id != cmd.instructor_id:
            raise AccessDeniedError(
                f"Instructor {cmd.instructor_id} is not authorized to grade this attempt"
            )

        if cmd.grade < 0 or cmd.grade > project.max_grade:
            raise InvalidGradeError(
                f"Grade {cmd.grade} is out of bounds (0-{project.max_grade})"
            )

        await self._attempts.update_grading(cmd.attempt_id, cmd.grade, cmd.feedback)
