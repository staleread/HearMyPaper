from uuid import UUID
from ..ports.incoming.manage_students import ManageStudentsPort
from ..ports.outgoing.education import EducationPort


class ManageStudentsUseCase(ManageStudentsPort):
    def __init__(self, education: EducationPort):
        self.education = education

    async def get_students(self, project_id: UUID) -> list[str]:
        return await self.education.get_project_students(project_id)

    async def assign_student(self, project_id: UUID, student_id: str) -> None:
        return await self.education.assign_student(project_id, student_id)

    async def remove_student(self, project_id: UUID, student_id: str) -> None:
        return await self.education.remove_student(project_id, student_id)
