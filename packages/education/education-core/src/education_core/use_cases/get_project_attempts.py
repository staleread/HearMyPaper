from uuid import UUID
from ..models import LabAttempt
from ..ports.incoming.get_project_attempts import GetProjectAttemptsPort
from ..ports.outgoing.attempt_repository import AttemptRepositoryPort


class GetProjectAttemptsUseCase(GetProjectAttemptsPort):
    def __init__(self, attempts: AttemptRepositoryPort):
        self._attempts = attempts

    async def __call__(self, project_id: UUID) -> list[LabAttempt]:
        return await self._attempts.find_by_project(project_id)
