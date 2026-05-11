from ..ports.incoming.get_my_projects import GetMyProjectsPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class GetMyProjectsUseCase(GetMyProjectsPort):
    def __init__(self, education: EducationPort):
        self.education = education

    async def __call__(self) -> list[Project]:
        return await self.education.get_my_projects()
