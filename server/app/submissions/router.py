from typing import Annotated
from fastapi import APIRouter, Body, Query

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize
from app.audit.decorators import audit

from .dto import SubmissionCreateRequest, SubmissionResponse
from . import service

router = APIRouter(prefix="/submission", tags=["submission"])


# Створення submission (student)
@router.post("/")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def create_submission(
    request: Annotated[SubmissionCreateRequest, Body()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
):
    submission_id = service.create_submission(
        project_student_id=request.project_student_id,
        title=request.title,
        encrypted_content=request.encrypted_content,
        db=db,
    )
    return {"id": submission_id}


# Видалення submission (student)
@router.delete("/{submission_id}")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def delete_submission(
    submission_id: int, db: PostgresRunnerDep, subject: CurrentSubjectDep
):
    service.remove_submission(submission_id=submission_id, db=db)
    return {"status": "deleted"}


# Отримати список для UI (instructor)
@router.get("/")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def read_submissions(
    db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> list[SubmissionResponse]:
    rows = service.list_submissions_for_ui(db=db)
    # скорочуємо title до 27 символів + "..."
    for row in rows:
        if len(row["title"]) > 27:
            row["title"] = row["title"][:27] + "..."
    return [SubmissionResponse(**row) for row in rows]


# Отримати публічний ключ інструктора по project_id
@router.get("/instructor_key")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def get_instructor_key(
    project_id: Annotated[int, Query()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
):
    key = service.get_instructor_key(project_id=project_id, db=db)
    return {"public_key": key}


@router.post("/create_project_student")
@audit()
@authorize(AccessLevel.RESTRICTED)
async def create_project_student(db: PostgresRunnerDep, subject: CurrentSubjectDep):
    student_id = subject.id
    instructor_id = 1
    project_student_id = service.create_project_for_student(
        student_id, instructor_id, db=db
    )
    return {"project_student_id": project_student_id}
