from uuid import UUID
from ..ports.incoming.get_project import GetProjectPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class GetProjectUseCase(GetProjectPort):
    def __init__(self, education: EducationPort):
        self.education = education

    async def __call__(self, project_id: UUID) -> Project | None:
        return await self.education.get_project(project_id)
