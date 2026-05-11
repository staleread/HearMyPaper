from uuid import UUID
from ..ports.incoming.get_project_attempts import GetProjectAttemptsPort
from ..ports.outgoing.education import EducationPort
from ..models import LabAttempt


class GetProjectAttemptsUseCase(GetProjectAttemptsPort):
    def __init__(self, education: EducationPort):
        self.education = education

    async def __call__(self, project_id: UUID) -> list[LabAttempt]:
        return await self.education.get_project_attempts(project_id)
