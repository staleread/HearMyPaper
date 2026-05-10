from datetime import datetime
from ..ports.incoming.create_project import CreateProjectPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class CreateProjectUseCase(CreateProjectPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(
        self, title: str, description: str, deadline: datetime
    ) -> Project:
        return await self.education_port.create_project(title, description, deadline)
