from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class RequestSubmissionUploadCommand:
    student_id: str
    project_id: UUID
    file_extension: str


@dataclass(frozen=True)
class UploadUrlResponse:
    upload_url: str
    submission_id: UUID


class RequestUploadUrlPort(Protocol):
    async def __call__(
        self, cmd: RequestSubmissionUploadCommand
    ) -> UploadUrlResponse: ...
