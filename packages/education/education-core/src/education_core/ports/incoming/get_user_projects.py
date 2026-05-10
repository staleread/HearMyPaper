from typing import Protocol
from education_core.models import ProjectListItem


class GetUserProjectsPort(Protocol):
    async def __call__(self, user_id: str) -> list[ProjectListItem]: ...
