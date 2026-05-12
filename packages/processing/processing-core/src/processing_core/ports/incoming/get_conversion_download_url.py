from typing import Protocol
from uuid import UUID


class GetConversionDownloadUrlPort(Protocol):
    async def __call__(self, conversion_id: UUID) -> str: ...
