from typing import Protocol
from uuid import UUID


class FilePathResolverPort(Protocol):
    def get_submission_path(
        self, project_id: UUID, student_id: str, submission_id: UUID
    ) -> str: ...
