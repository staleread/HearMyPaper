from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class SubmissionUploadInfo:
    url: str
    submission_id: UUID
    filename: str
    extension: str


class SubmissionsPort(Protocol):
    async def request_upload_url(
        self, project_id: UUID, filename: str, extension: str
    ) -> SubmissionUploadInfo: ...

    async def commit_submission(self, submission_id: UUID) -> None: ...
