from uuid import UUID
from ..ports.incoming.get_project_attempts import GetProjectAttemptsPort
from ..ports.outgoing.education import EducationPort
from ..models import LabAttempt


class GetProjectAttemptsUseCase(GetProjectAttemptsPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(self, project_id: UUID) -> list[LabAttempt]:
        return await self.education_port.get_project_attempts(project_id)
