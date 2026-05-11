from typing import override
from uuid import UUID
from datetime import datetime

from blacksheep import Request, FromJSON, FromQuery
from blacksheep.server.controllers import Controller, get, post
from blacksheep.server.responses import (
    ok,
    not_found,
    forbidden,
    status_code,
    no_content,
)
from blacksheep.server.authorization import auth
from pydantic import BaseModel

from education_core.exceptions import (
    AccessDeniedError,
    AttemptNotFoundError,
    ProjectNotFoundError,
    AttemptAlreadyGradedError,
    InvalidGradeError,
)
from education_core.ports.incoming import (
    GetProjectAttemptsPort,
    ViewSubmissionPort,
    GradeLabAttemptPort,
    GradeLabAttemptCommand,
    GetLabAttemptPort,
)


class AttemptListItemResponse(BaseModel):
    attempt_id: UUID
    student_id: str
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None


class GradeAttemptRequest(BaseModel):
    grade: int
    feedback: str | None = None


class AttemptResponse(BaseModel):
    attempt_id: UUID
    student_id: str
    project_id: UUID
    submission_id: UUID
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None
    instructor_feedback: str | None = None


class Attempts(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/attempts"

    def __init__(
        self,
        get_project_attempts_port: GetProjectAttemptsPort,
        view_submission_port: ViewSubmissionPort,
        grade_lab_attempt_port: GradeLabAttemptPort,
        get_lab_attempt_port: GetLabAttemptPort,
    ) -> None:
        self.get_project_attempts_port = get_project_attempts_port
        self.view_submission_port = view_submission_port
        self.grade_lab_attempt_port = grade_lab_attempt_port
        self.get_lab_attempt_port = get_lab_attempt_port

    @auth()
    @get("/{attempt_id}")
    async def get_attempt(self, attempt_id: UUID):
        try:
            a = await self.get_lab_attempt_port(attempt_id)
            return ok(
                AttemptResponse(
                    attempt_id=a.attempt_id,
                    student_id=a.student_id,
                    project_id=a.project_id,
                    submission_id=a.submission_id,
                    submitted_at=a.submitted_at,
                    is_on_time=a.is_on_time,
                    grade=a.grade,
                    instructor_feedback=a.instructor_feedback,
                )
            )
        except AttemptNotFoundError as e:
            return not_found(str(e))

    @auth()
    @get("")
    async def get_attempts(self, project_id: FromQuery[UUID]):
        if project_id.value is None:
            return status_code(400, "Missing project_id query parameter")

        attempts = await self.get_project_attempts_port(project_id.value)
        return ok(
            [
                AttemptListItemResponse(
                    attempt_id=a.attempt_id,
                    student_id=a.student_id,
                    submitted_at=a.submitted_at,
                    is_on_time=a.is_on_time,
                    grade=a.grade,
                )
                for a in attempts
            ]
        )

    @auth()
    @get("/{attempt_id}/download-url")
    async def get_download_url(self, request: Request, attempt_id: UUID):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not found in token")

        try:
            info = await self.view_submission_port(user_id, attempt_id)
            return ok(
                {
                    "download_url": info.url,
                    "filename": info.filename,
                    "extension": info.extension,
                }
            )
        except AttemptNotFoundError as e:
            return not_found(str(e))
        except ProjectNotFoundError as e:
            return not_found(str(e))
        except AccessDeniedError as e:
            return forbidden(str(e))

    @auth()
    @post("/{attempt_id}/grade")
    async def grade_attempt(
        self,
        request: Request,
        attempt_id: UUID,
        data: FromJSON[GradeAttemptRequest],
    ):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not found in token")

        req = data.value
        cmd = GradeLabAttemptCommand(
            attempt_id=attempt_id,
            instructor_id=user_id,
            grade=req.grade,
            feedback=req.feedback,
        )
        try:
            await self.grade_lab_attempt_port(cmd)
            return no_content()
        except AttemptNotFoundError as e:
            return not_found(str(e))
        except (AttemptAlreadyGradedError, InvalidGradeError) as e:
            return status_code(400, str(e))
        except AccessDeniedError as e:
            return forbidden(str(e))
