from typing import Protocol
from datetime import datetime
from ...models import Project


class CreateProjectPort(Protocol):
    async def __call__(
        self, title: str, description: str, deadline: datetime
    ) -> Project: ...
