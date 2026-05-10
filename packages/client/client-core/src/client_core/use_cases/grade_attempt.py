from uuid import UUID
from ..ports.incoming.grade_attempt import GradeAttemptPort
from ..ports.outgoing.education import EducationPort


class GradeAttemptUseCase(GradeAttemptPort):
    def __init__(self, education_port: EducationPort):
        self.education_port = education_port

    async def __call__(
        self, attempt_id: UUID, grade: int, feedback: str | None
    ) -> None:
        return await self.education_port.grade_attempt(attempt_id, grade, feedback)
