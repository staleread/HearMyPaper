from typing import Protocol
from uuid import UUID


class DownloadAttemptPort(Protocol):
    async def __call__(self, attempt_id: UUID, password: str) -> str:
        """Downloads the lab attempt, unseals it with the provided password, and returns the local file path."""
        ...
