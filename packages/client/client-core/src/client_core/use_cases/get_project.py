from uuid import UUID
from ..ports.incoming.get_project import GetProjectPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class GetProjectUseCase(GetProjectPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(self, project_id: UUID) -> Project:
        return await self.education_port.get_project(project_id)
