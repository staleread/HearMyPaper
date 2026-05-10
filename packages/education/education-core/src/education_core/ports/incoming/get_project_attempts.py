from typing import Protocol
from uuid import UUID
from education_core.models import AttemptListItem


class GetProjectAttemptsPort(Protocol):
    async def __call__(self, project_id: UUID) -> list[AttemptListItem]:
        """Returns a summarized list of attempts for a given project."""
        ...
