from ..ports.incoming.get_my_projects import GetMyProjectsPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class GetMyProjectsUseCase(GetMyProjectsPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(self) -> list[Project]:
        return await self.education_port.get_my_projects()
