from uuid import UUID
from ..ports.incoming.grade_attempt import GradeAttemptPort
from ..ports.outgoing.education import EducationPort


class GradeAttemptUseCase(GradeAttemptPort):
    def __init__(self, education: EducationPort):
        self.education = education

    async def __call__(
        self, attempt_id: UUID, grade: int, feedback: str | None
    ) -> None:
        return await self.education.grade_attempt(attempt_id, grade, feedback)
