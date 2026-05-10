from typing import Protocol
from ...models import ProjectListItem


class GetUserProjectsPort(Protocol):
    async def __call__(self, user_id: str) -> list[ProjectListItem]: ...
