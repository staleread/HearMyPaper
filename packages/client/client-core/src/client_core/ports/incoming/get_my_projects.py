from typing import Protocol
from ...models import Project


class GetMyProjectsPort(Protocol):
    async def __call__(self) -> list[Project]: ...
