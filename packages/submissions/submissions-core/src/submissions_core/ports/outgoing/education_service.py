from typing import Protocol
from uuid import UUID


class EducationServicePort(Protocol):
    async def verify_project_exists(self, project_id: UUID) -> bool: ...
    async def verify_student_belongs_to_project(
        self, student_id: str, project_id: UUID
    ) -> bool: ...
