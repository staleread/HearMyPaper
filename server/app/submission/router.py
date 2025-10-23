from typing import Annotated
import cbor2
from fastapi import APIRouter, Body, Query, Request
from fastapi.responses import Response as FastAPIResponse

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize
from app.audit.decorators import audit

from .dto import SubmissionResponse, SubmissionHashResponse
from . import service

router = APIRouter()


@router.post("/")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def create_submission(
    body: Annotated[bytes, Body()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
    request: Request,
):
    try:
        data = cbor2.loads(body)
        project_id = data["project_id"]
        title = data["title"]
        encrypted_content = data["encrypted_content"]

        submission_id = service.create_submission(
            project_id=project_id,
            student_id=subject.id,
            title=title,
            encrypted_content=encrypted_content,
            db=db,
        )
        return {"id": submission_id}
    except (KeyError, cbor2.CBORDecodeError) as e:
        return {"error": f"Invalid CBOR data: {e}"}, 400


@router.delete("/{submission_id}")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def delete_submission(
    submission_id: int,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
    request: Request,
):
    service.remove_submission(submission_id=submission_id, db=db)
    return {"status": "deleted"}


@router.get("/")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def read_submissions(
    db: PostgresRunnerDep, subject: CurrentSubjectDep, request: Request
) -> list[SubmissionResponse]:
    rows = service.list_submissions_for_ui(db=db)
    for row in rows:
        if len(row["title"]) > 27:
            row["title"] = row["title"][:27] + "..."
    return [SubmissionResponse(**row) for row in rows]


@router.get("/instructor_key")
@audit()
@authorize(AccessLevel.UNCLASSIFIED)
async def read_instructor_key(
    project_id: Annotated[int, Query()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
    request: Request,
):
    key = service.get_instructor_key(project_id=project_id, db=db)
    return {"public_key": key}


@router.get("/{submission_id}/hash")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def read_submission_hash(
    submission_id: int,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
    request: Request,
) -> SubmissionHashResponse:
    content_hash = service.get_submission_hash(submission_id=submission_id, db=db)
    return SubmissionHashResponse(content_hash=content_hash)


@router.get("/{submission_id}/content")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def read_submission_content(
    submission_id: int,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
    request: Request,
):
    encrypted_content = service.get_submission_content(
        submission_id=submission_id, db=db
    )
    return FastAPIResponse(
        content=encrypted_content, media_type="application/octet-stream"
    )
