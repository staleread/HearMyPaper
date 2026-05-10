from uuid import UUID
from ..ports.incoming.get_attempt import GetAttemptPort
from ..ports.outgoing.education import EducationPort
from ..models import LabAttempt


class GetAttemptUseCase(GetAttemptPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(self, attempt_id: UUID) -> LabAttempt | None:
        return await self.education_port.get_attempt(attempt_id)
