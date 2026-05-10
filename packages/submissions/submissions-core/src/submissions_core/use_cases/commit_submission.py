from datetime import datetime, UTC
from shared_kernel.events import SubmissionCommittedEvent
from ..models import SubmissionStatus
from ..exceptions import (
    SubmissionNotFoundError,
    UnauthorizedSubmissionError,
    InvalidSubmissionStatusError,
)
from ..ports.incoming.commit_submission import (
    CommitSubmissionPort,
    CommitSubmissionCommand,
)
from ..ports.outgoing.submission_repository import SubmissionRepositoryPort
from ..ports.outgoing.event_publisher import EventPublisherPort


class CommitSubmissionUseCase(CommitSubmissionPort):
    def __init__(
        self, submissions: SubmissionRepositoryPort, publisher: EventPublisherPort
    ):
        self._submissions = submissions
        self._publisher = publisher

    async def __call__(self, cmd: CommitSubmissionCommand) -> None:
        submission = await self._submissions.find_by_id(cmd.submission_id)
        if not submission:
            raise SubmissionNotFoundError(f"Submission {cmd.submission_id} not found")

        if submission.student_id != cmd.student_id:
            raise UnauthorizedSubmissionError(
                f"Submission {cmd.submission_id} does not belong to student {cmd.student_id}"
            )

        if submission.status != SubmissionStatus.PENDING_UPLOAD:
            raise InvalidSubmissionStatusError(
                f"Submission {cmd.submission_id} is in status {submission.status}, cannot commit"
            )

        await self._submissions.update_status(
            cmd.submission_id, SubmissionStatus.COMMITTED
        )

        event = SubmissionCommittedEvent(
            submission_id=submission.submission_id,
            student_id=submission.student_id,
            project_id=submission.project_id,
            timestamp=datetime.now(UTC),
        )
        await self._publisher.publish_submission_committed(event)
