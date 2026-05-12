from typing import Protocol
from uuid import UUID


class ConvertAttemptToAudioPort(Protocol):
    async def __call__(self, attempt_id: UUID, file_path: str) -> None: ...
