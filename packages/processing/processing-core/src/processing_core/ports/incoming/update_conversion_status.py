from typing import Protocol
from uuid import UUID


class UpdateConversionStatusPort(Protocol):
    async def __call__(self, task_id: UUID, status: str) -> None: ...
