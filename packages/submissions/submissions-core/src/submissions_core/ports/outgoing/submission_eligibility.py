from typing import Protocol
from uuid import UUID


class SubmissionEligibilityPort(Protocol):
    async def can_student_submit(self, student_id: str, project_id: UUID) -> bool:
        """Check if the student is eligible to submit for the project (deadline, attempt count, etc)."""
        ...
