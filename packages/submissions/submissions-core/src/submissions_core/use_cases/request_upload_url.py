from uuid import uuid4
from datetime import datetime, UTC
from ..models import LabSubmission, SubmissionStatus
from ..exceptions import (
    AccessDeniedError,
)
from ..ports.incoming.request_upload_url import (
    RequestUploadUrlPort,
    RequestSubmissionUploadCommand,
    UploadUrlResponse,
)
from ..ports.outgoing.submission_repository import SubmissionRepositoryPort
from ..ports.outgoing.storage import StoragePort
from ..ports.outgoing.submission_eligibility import SubmissionEligibilityPort


class RequestUploadUrlUseCase(RequestUploadUrlPort):
    def __init__(
        self,
        submissions: SubmissionRepositoryPort,
        storage: StoragePort,
        eligibility: SubmissionEligibilityPort,
    ):
        self._submissions = submissions
        self._storage = storage
        self._eligibility = eligibility

    async def __call__(self, cmd: RequestSubmissionUploadCommand) -> UploadUrlResponse:
        if not await self._eligibility.can_student_submit(
            cmd.student_id, cmd.project_id
        ):
            raise AccessDeniedError(
                f"Student {cmd.student_id} is not allowed to submit for project {cmd.project_id}"
            )

        submission_id = uuid4()
        extension = cmd.file_extension.lstrip(".")
        path = f"{cmd.project_id}/{cmd.student_id}/{submission_id}.{extension}"

        upload_url = await self._storage.generate_upload_url(
            path, content_type="application/octet-stream"
        )

        submission = LabSubmission(
            submission_id=submission_id,
            student_id=cmd.student_id,
            project_id=cmd.project_id,
            storage_path=path,
            status=SubmissionStatus.PENDING_UPLOAD,
            created_at=datetime.now(UTC),
            metadata={"file_extension": extension},
        )

        await self._submissions.save(submission)

        return UploadUrlResponse(
            upload_url=upload_url,
            submission_id=submission_id,
        )
