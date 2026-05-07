from typing import Protocol
from ...models import Project


class GetUserProjectsPort(Protocol):
    async def __call__(self, user_id: str) -> list[Project]: ...
