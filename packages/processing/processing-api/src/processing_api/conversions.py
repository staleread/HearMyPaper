from datetime import datetime
from typing import override
from uuid import UUID

from blacksheep import FromJSON, Request
from blacksheep.server.controllers import Controller, post
from blacksheep.server.responses import ok, status_code, not_found
from blacksheep.server.authorization import auth
from pydantic import BaseModel

from orchestrator_core.exceptions import NoWorkerAvailableError
from processing_core.exceptions import (
    ConversionNotFoundError,
    FileNotUploadedError,
    InvalidConversionStatusError,
)
from processing_core.models import ProcessingTaskType
from processing_core.ports.incoming.request_conversion import (
    RequestConversionPort,
    RequestConversionQuery,
)
from processing_core.ports.incoming.commit_conversion import (
    CommitConversionPort,
    CommitConversionCommand,
)


class RequestConversionRequest(BaseModel):
    lab_attempt_id: UUID
    task_type: ProcessingTaskType


class RequestConversionResponse(BaseModel):
    assignment_id: UUID
    worker_id: UUID
    worker_public_key: bytes
    upload_url: str
    expires_at: datetime


class Conversions(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/conversions"

    def __init__(
        self,
        request_conversion: RequestConversionPort,
        commit_conversion: CommitConversionPort,
    ):
        self.request_conversion = request_conversion
        self.commit_conversion = commit_conversion

    @auth()
    @post("/")
    async def request_conversion_endpoint(
        self, request: Request, data: FromJSON[RequestConversionRequest]
    ):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not found in token")

        req = data.value
        query = RequestConversionQuery(
            lab_attempt_id=req.lab_attempt_id,
            instructor_id=user_id,
            task_type=req.task_type,
        )

        try:
            resp = await self.request_conversion(query)
            return ok(
                RequestConversionResponse(
                    assignment_id=resp.assignment_id,
                    worker_id=resp.worker_id,
                    worker_public_key=resp.worker_public_key,
                    upload_url=resp.upload_url,
                    expires_at=resp.expires_at,
                )
            )
        except NoWorkerAvailableError as e:
            return status_code(503, str(e))
        except Exception as e:
            return status_code(500, str(e))

    @auth()
    @post("/{conversion_id}/commit")
    async def commit_conversion_endpoint(self, conversion_id: UUID):
        command = CommitConversionCommand(conversion_id=conversion_id)
        try:
            await self.commit_conversion(command)
            return ok()
        except ConversionNotFoundError as e:
            return not_found(str(e))
        except FileNotUploadedError as e:
            return status_code(400, str(e))
        except InvalidConversionStatusError as e:
            return status_code(409, str(e))
        except Exception as e:
            return status_code(500, str(e))
