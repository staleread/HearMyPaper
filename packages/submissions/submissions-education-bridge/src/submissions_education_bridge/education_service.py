from typing import override
from uuid import UUID

from education_core.ports.outgoing.project_repository import ProjectRepositoryPort
from education_core.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)
from submissions_core.ports.outgoing.education_service import EducationServicePort


class EducationServiceAdapter(EducationServicePort):
    def __init__(
        self, projects: ProjectRepositoryPort, students: ProjectStudentRepositoryPort
    ):
        self._projects = projects
        self._students = students

    @override
    async def verify_project_exists(self, project_id: UUID) -> bool:
        project = await self._projects.get_by_id(project_id)
        return project is not None

    @override
    async def verify_student_belongs_to_project(
        self, student_id: str, project_id: UUID
    ) -> bool:
        return await self._students.is_student_assigned(project_id, student_id)
