from typing import Protocol
from datetime import datetime
from uuid import UUID
from ...models import Project


class UpdateProjectPort(Protocol):
    async def __call__(
        self,
        project_id: UUID,
        title: str,
        description: str,
        instructor_id: str,
        deadline: datetime,
    ) -> Project: ...
