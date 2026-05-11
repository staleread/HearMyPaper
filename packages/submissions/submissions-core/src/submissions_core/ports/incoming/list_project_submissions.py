from typing import Protocol
from uuid import UUID
from ...models import SubmissionListItem


class ListProjectSubmissionsPort(Protocol):
    async def __call__(self, project_id: UUID) -> list[SubmissionListItem]: ...
