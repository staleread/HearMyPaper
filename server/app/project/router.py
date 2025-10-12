from typing import Annotated
from fastapi import APIRouter, Path

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize
from app.audit.decorators import audit

from .dto import (
    ProjectResponse,
    ProjectListResponse,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectCreateResponse,
    StudentAssignmentRequest,
    ProjectStudentResponse,
)
from . import service as project_service

router = APIRouter()


@router.get("/")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def read_projects(
    db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> list[ProjectListResponse]:
    """Get simplified list of all projects with only essential fields"""
    rows = db.query("""
        SELECT p.id, p.title, CONCAT(u.name, ' ', u.surname) as instructor_full_name, p.deadline
        FROM projects p
        JOIN users u ON p.instructor_id = u.id
        ORDER BY p.deadline DESC, p.id
    """).many_rows()

    return [
        ProjectListResponse(
            id=row["id"],
            title=row["title"],
            instructor_full_name=row["instructor_full_name"],
            deadline=row["deadline"],
        )
        for row in rows
    ]


@router.get("/{id}")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def read_project(
    id: Annotated[int, Path()], db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> ProjectResponse:
    return project_service.get_project_by_id(id, db=db)


@router.post("/")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def create_project(
    req: ProjectCreateRequest, db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> ProjectCreateResponse:
    return project_service.create_project(req, db=db)


@router.put("/{id}")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def update_project(
    id: Annotated[int, Path()],
    req: ProjectUpdateRequest,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
) -> ProjectResponse:
    return project_service.update_project(id, req, db=db)


@router.put("/{id}/students")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def update_project_students(
    id: Annotated[int, Path()],
    req: StudentAssignmentRequest,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
) -> ProjectResponse:
    return project_service.assign_students_to_project(id, req, db=db)


@router.get("/{id}/students")
@authorize(AccessLevel.CONTROLLED)
@audit()
async def read_project_students(
    id: Annotated[int, Path()], db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> list[ProjectStudentResponse]:
    """Get students assigned to a project with their id and full name for dropdown/list purposes"""
    rows = (
        db.query("""
        SELECT u.id, CONCAT(u.name, ' ', u.surname) as username
        FROM project_students ps
        JOIN users u ON ps.student_id = u.id
        WHERE ps.project_id = :project_id
        ORDER BY u.surname, u.name
    """)
        .bind(project_id=id)
        .many_rows()
    )

    return [
        ProjectStudentResponse(
            id=row["id"],
            username=row["username"],
        )
        for row in rows
    ]
