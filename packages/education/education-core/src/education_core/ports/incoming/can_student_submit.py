from typing import Protocol
from uuid import UUID


class CanStudentSubmitPort(Protocol):
    async def __call__(self, student_id: str, project_id: UUID) -> bool:
        """Checks if a student can submit for a project."""
        ...
