from uuid import uuid4
from datetime import datetime, UTC
from ..models import LabSubmission, SubmissionStatus
from ..exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    SubmissionAlreadyExistsError,
)
from ..ports.incoming.request_upload_url import (
    RequestUploadUrlPort,
    RequestSubmissionUploadCommand,
)
from ..ports.outgoing.submission_repository import SubmissionRepositoryPort
from ..ports.outgoing.storage import StoragePort
from ..ports.outgoing.education_service import EducationServicePort


class RequestUploadUrlUseCase(RequestUploadUrlPort):
    def __init__(
        self,
        submissions: SubmissionRepositoryPort,
        storage: StoragePort,
        education: EducationServicePort,
    ):
        self._submissions = submissions
        self._storage = storage
        self._education = education

    async def __call__(self, cmd: RequestSubmissionUploadCommand) -> str:
        if not await self._education.verify_project_exists(cmd.project_id):
            raise ProjectNotFoundError(f"Project {cmd.project_id} not found")

        if not await self._education.verify_student_belongs_to_project(
            cmd.student_id, cmd.project_id
        ):
            raise StudentNotFoundError(
                f"Student {cmd.student_id} is not assigned to project {cmd.project_id}"
            )

        existing = await self._submissions.find_by_student_and_project(
            cmd.student_id, cmd.project_id
        )
        if existing and existing.status == SubmissionStatus.COMMITTED:
            raise SubmissionAlreadyExistsError(
                f"Student {cmd.student_id} already submitted for project {cmd.project_id}"
            )

        submission_id = uuid4()
        extension = cmd.file_extension.lstrip(".")
        path = (
            f"submissions/{cmd.project_id}/{cmd.student_id}/{submission_id}.{extension}"
        )

        upload_url = await self._storage.generate_upload_url(path)

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

        return upload_url
