from typing import Protocol
from uuid import UUID


class DownloadAttemptPort(Protocol):
    async def __call__(self, attempt_id: UUID, download_folder: str) -> str:
        """Downloads the lab attempt to the specified folder and returns the local file path."""
        ...
