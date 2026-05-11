from typing import override
from uuid import UUID

from education_core.ports.incoming.can_student_submit import CanStudentSubmitPort
from submissions_core.ports.outgoing.submission_eligibility import (
    SubmissionEligibilityPort,
)


class EducationServiceAdapter(SubmissionEligibilityPort):
    def __init__(self, can_submit: CanStudentSubmitPort):
        self._can_submit = can_submit

    @override
    async def can_student_submit(self, student_id: str, project_id: UUID) -> bool:
        return await self._can_submit(student_id, project_id)
