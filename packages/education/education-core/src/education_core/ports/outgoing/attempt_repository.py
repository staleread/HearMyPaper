from typing import Protocol
from uuid import UUID
from ...models import LabAttempt


class AttemptRepositoryPort(Protocol):
    async def save(self, attempt: LabAttempt) -> None: ...
    async def find_by_student_and_project(
        self, student_id: str, project_id: UUID
    ) -> LabAttempt | None: ...
    async def get_by_submission_id(self, submission_id: UUID) -> LabAttempt | None: ...
