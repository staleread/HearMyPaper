from typing import Protocol
from uuid import UUID


class SubmissionsPort(Protocol):
    async def request_upload_url(
        self, project_id: UUID, file_extension: str
    ) -> tuple[str, UUID]: ...
    async def commit_submission(self, submission_id: UUID) -> None: ...
