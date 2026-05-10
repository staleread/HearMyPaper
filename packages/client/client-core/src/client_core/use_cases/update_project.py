from datetime import datetime
from uuid import UUID
from ..ports.incoming.update_project import UpdateProjectPort
from ..ports.outgoing.education import EducationPort
from ..models import Project


class UpdateProjectUseCase(UpdateProjectPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(
        self, project_id: UUID, title: str, description: str, deadline: datetime
    ) -> Project:
        return await self.education_port.update_project(
            project_id, title, description, deadline
        )
