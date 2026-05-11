from uuid import UUID
from ..models import SubmissionListItem
from ..ports.incoming.list_project_submissions import ListProjectSubmissionsPort
from ..ports.outgoing.submission_repository import SubmissionRepositoryPort


class ListProjectSubmissionsUseCase(ListProjectSubmissionsPort):
    def __init__(self, submissions: SubmissionRepositoryPort):
        self._submissions = submissions

    async def __call__(self, project_id: UUID) -> list[SubmissionListItem]:
        return await self._submissions.list_by_project(project_id)
