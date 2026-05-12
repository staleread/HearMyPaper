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


from submissions_core.ports.outgoing.path_resolver import FilePathResolverPort


class RequestUploadUrlUseCase(RequestUploadUrlPort):
    def __init__(
        self,
        submissions: SubmissionRepositoryPort,
        storage: StoragePort,
        eligibility: SubmissionEligibilityPort,
        paths: FilePathResolverPort,
    ):
        self._submissions = submissions
        self._storage = storage
        self._eligibility = eligibility
        self._paths = paths

    async def __call__(self, cmd: RequestSubmissionUploadCommand) -> UploadUrlResponse:
        if not await self._eligibility.can_student_submit(
            cmd.student_id, cmd.project_id
        ):
            raise AccessDeniedError(
                f"Student {cmd.student_id} is not allowed to submit for project {cmd.project_id}"
            )

        submission_id = uuid4()
        extension = cmd.extension.lstrip(".")
        # Files on cloud storage always have .bin extension
        path = self._paths.get_submission_path(
            cmd.project_id, cmd.student_id, submission_id
        )

        upload_url = await self._storage.generate_upload_url(path)

        submission = LabSubmission(
            submission_id=submission_id,
            student_id=cmd.student_id,
            project_id=cmd.project_id,
            storage_path=path,
            status=SubmissionStatus.PENDING_UPLOAD,
            created_at=datetime.now(UTC),
            filename=cmd.filename,
            extension=extension,
            metadata={},
        )

        await self._submissions.save(submission)

        return UploadUrlResponse(
            upload_url=upload_url,
            submission_id=submission_id,
            filename=cmd.filename,
            extension=extension,
        )
