from uuid import UUID
from ..models import LabSubmission
from ..exceptions import SubmissionNotFoundError
from ..ports.incoming.get_submission import GetSubmissionPort
from ..ports.outgoing.submission_repository import SubmissionRepositoryPort


class GetSubmissionUseCase(GetSubmissionPort):
    def __init__(self, submissions: SubmissionRepositoryPort):
        self._submissions = submissions

    async def __call__(self, submission_id: UUID) -> LabSubmission:
        submission = await self._submissions.find_by_id(submission_id)
        if not submission:
            raise SubmissionNotFoundError(f"Submission {submission_id} not found")
        return submission
