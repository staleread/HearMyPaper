from typing import Protocol
from uuid import UUID


class UploadSubmissionPort(Protocol):
    async def __call__(self, project_id: UUID, file_path: str) -> None: ...
