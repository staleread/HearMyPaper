from uuid import uuid4
from ..models import LabAttempt
from ..ports.incoming.register_attempt import (
    RegisterAttemptPort,
    RegisterAttemptCommand,
)
from ..ports.outgoing.project_repository import ProjectRepositoryPort
from ..ports.outgoing.attempt_repository import AttemptRepositoryPort
from ..exceptions import ProjectNotFoundError


class RegisterAttemptUseCase(RegisterAttemptPort):
    def __init__(
        self,
        projects: ProjectRepositoryPort,
        attempts: AttemptRepositoryPort,
    ):
        self._projects = projects
        self._attempts = attempts

    async def __call__(self, cmd: RegisterAttemptCommand) -> None:
        project = await self._projects.get_by_id(cmd.project_id)
        if not project:
            # This should ideally not happen if data integrity is maintained
            raise ProjectNotFoundError(f"Project {cmd.project_id} not found")

        is_on_time = cmd.timestamp <= project.deadline

        attempt = LabAttempt(
            attempt_id=uuid4(),
            student_id=cmd.student_id,
            project_id=cmd.project_id,
            submission_id=cmd.submission_id,
            submitted_at=cmd.timestamp,
            is_on_time=is_on_time,
        )

        await self._attempts.save(attempt)
