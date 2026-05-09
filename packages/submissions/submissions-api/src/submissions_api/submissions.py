from datetime import datetime
from typing import override
from uuid import UUID

from blacksheep import FromJSON
from blacksheep.server.controllers import Controller, get, post
from blacksheep.server.responses import ok, not_found, status_code, forbidden
from pydantic import BaseModel

from submissions_core.exceptions import (
    SubmissionNotFoundError,
    SubmissionAlreadyExistsError,
    InvalidSubmissionStatusError,
    UnauthorizedSubmissionError,
    ProjectNotFoundError,
    StudentNotFoundError,
)
from submissions_core.ports.incoming import (
    RequestUploadUrlPort,
    RequestSubmissionUploadCommand,
    CommitSubmissionPort,
    CommitSubmissionCommand,
    GetSubmissionPort,
    ListProjectSubmissionsPort,
)


class RequestUploadUrlRequest(BaseModel):
    project_id: UUID
    file_extension: str


class SubmissionResponse(BaseModel):
    submission_id: UUID
    student_id: str
    project_id: UUID
    storage_path: str
    status: str
    created_at: datetime
    metadata: dict[str, str]


class SubmissionsController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/submissions"

    def __init__(
        self,
        request_upload_url_port: RequestUploadUrlPort,
        commit_submission_port: CommitSubmissionPort,
        get_submission_port: GetSubmissionPort,
        list_project_submissions_port: ListProjectSubmissionsPort,
    ):
        self.request_upload_url_port = request_upload_url_port
        self.commit_submission_port = commit_submission_port
        self.get_submission_port = get_submission_port
        self.list_project_submissions_port = list_project_submissions_port

    @post("/upload-url")
    async def request_upload_url(
        self, user_id: str, data: FromJSON[RequestUploadUrlRequest]
    ):
        req = data.value
        cmd = RequestSubmissionUploadCommand(
            student_id=user_id,
            project_id=req.project_id,
            file_extension=req.file_extension,
        )
        try:
            url = await self.request_upload_url_port(cmd)
            return ok({"upload_url": url})
        except (ProjectNotFoundError, StudentNotFoundError) as e:
            return not_found(str(e))
        except SubmissionAlreadyExistsError as e:
            return status_code(409, str(e))

    @post("/{submission_id}/commit")
    async def commit_submission(self, submission_id: UUID, user_id: str):
        cmd = CommitSubmissionCommand(
            submission_id=submission_id,
            student_id=user_id,
        )
        try:
            await self.commit_submission_port(cmd)
            return ok()
        except SubmissionNotFoundError as e:
            return not_found(str(e))
        except UnauthorizedSubmissionError as e:
            return forbidden(str(e))
        except InvalidSubmissionStatusError as e:
            return status_code(400, str(e))

    @get("/{submission_id}")
    async def get_submission(self, submission_id: UUID):
        try:
            s = await self.get_submission_port(submission_id)
            return ok(
                SubmissionResponse(
                    submission_id=s.submission_id,
                    student_id=s.student_id,
                    project_id=s.project_id,
                    storage_path=s.storage_path,
                    status=s.status.value,
                    created_at=s.created_at,
                    metadata=s.metadata,
                )
            )
        except SubmissionNotFoundError as e:
            return not_found(str(e))

    @get("/project/{project_id}")
    async def list_submissions(self, project_id: UUID):
        submissions = await self.list_project_submissions_port(project_id)
        return ok(
            [
                SubmissionResponse(
                    submission_id=s.submission_id,
                    student_id=s.student_id,
                    project_id=s.project_id,
                    storage_path=s.storage_path,
                    status=s.status.value,
                    created_at=s.created_at,
                    metadata=s.metadata,
                )
                for s in submissions
            ]
        )
