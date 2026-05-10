from typing import Protocol
from uuid import UUID
from ...models import AttemptListItem


class GetProjectAttemptsPort(Protocol):
    async def __call__(self, project_id: UUID) -> list[AttemptListItem]:
        """Returns all attempts for a given project."""
        ...
