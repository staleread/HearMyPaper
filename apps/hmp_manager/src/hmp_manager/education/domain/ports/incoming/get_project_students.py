from typing import Protocol
from uuid import UUID


class GetProjectStudentsPort(Protocol):
    async def __call__(self, project_id: UUID) -> list[str]: ...
