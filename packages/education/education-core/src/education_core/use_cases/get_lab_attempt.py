from uuid import UUID
from education_core.models import LabAttempt
from education_core.ports.incoming.get_lab_attempt import GetLabAttemptPort
from education_core.ports.outgoing.attempt_repository import AttemptRepositoryPort
from education_core.exceptions import AttemptNotFoundError


class GetLabAttemptUseCase(GetLabAttemptPort):
    def __init__(self, attempt_repo: AttemptRepositoryPort):
        self.attempt_repo = attempt_repo

    async def __call__(self, attempt_id: UUID) -> LabAttempt:
        attempt = await self.attempt_repo.get_by_id(attempt_id)
        if not attempt:
            raise AttemptNotFoundError(attempt_id)
        return attempt
