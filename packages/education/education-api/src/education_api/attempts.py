from uuid import UUID
from datetime import datetime
from typing import override

from blacksheep import Request, FromJSON
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


class AttemptsController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/projects/{project_id}/attempts"

    def __init__(
        self,
        get_project_attempts_port: GetProjectAttemptsPort,
        view_submission_port: ViewSubmissionPort,
        grade_lab_attempt_port: GradeLabAttemptPort,
    ) -> None:
        self.get_project_attempts_port = get_project_attempts_port
        self.view_submission_port = view_submission_port
        self.grade_lab_attempt_port = grade_lab_attempt_port

    @auth()
    @get("/")
    async def get_attempts(self, project_id: UUID):
        attempts = await self.get_project_attempts_port(project_id)
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
    @get("/{submission_id}/download-url")
    async def get_download_url(
        self, request: Request, project_id: UUID, submission_id: UUID
    ):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not token")

        try:
            url = await self.view_submission_port(user_id, submission_id)
            return ok({"download_url": url})
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
        project_id: UUID,
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
