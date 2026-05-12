from typing import Protocol
from uuid import UUID


class RequestAttemptConversionPort(Protocol):
    async def __call__(self, source_id: UUID, file_path: str) -> None: ...
