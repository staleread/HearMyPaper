from uuid import UUID
from typing import Protocol


class DownloadConversionPort(Protocol):
    async def __call__(self, conversion_id: UUID, password: str) -> str: ...
