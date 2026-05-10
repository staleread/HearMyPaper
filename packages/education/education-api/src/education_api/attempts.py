from uuid import UUID
from datetime import datetime
from typing import override, Optional

from blacksheep.server.controllers import Controller, get
from blacksheep.server.responses import ok, not_found, forbidden
from pydantic import BaseModel

from education_core.exceptions import (
    AccessDeniedError,
    AttemptNotFoundError,
    ProjectNotFoundError,
)
from education_core.ports.incoming import (
    GetProjectAttemptsPort,
    ViewSubmissionPort,
)


class AttemptResponse(BaseModel):
    attempt_id: UUID
    student_id: str
    project_id: UUID
    submission_id: UUID
    submitted_at: datetime
    is_on_time: bool
    grade: Optional[int] = None
    instructor_feedback: Optional[str] = None


class AttemptsController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/projects/{project_id}/attempts"

    def __init__(
        self,
        get_project_attempts_port: GetProjectAttemptsPort,
        view_submission_port: ViewSubmissionPort,
    ) -> None:
        self.get_project_attempts_port = get_project_attempts_port
        self.view_submission_port = view_submission_port

    @get("/")
    async def get_attempts(self, project_id: UUID):
        attempts = await self.get_project_attempts_port(project_id)
        return ok(
            [
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
                for a in attempts
            ]
        )

    @get("/{submission_id}/download-url")
    async def get_download_url(
        self, project_id: UUID, submission_id: UUID, user_id: str
    ):
        try:
            url = await self.view_submission_port(user_id, submission_id)
            return ok({"download_url": url})
        except AttemptNotFoundError as e:
            return not_found(str(e))
        except ProjectNotFoundError as e:
            return not_found(str(e))
        except AccessDeniedError as e:
            return forbidden(str(e))
