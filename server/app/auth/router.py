from typing import Annotated
from fastapi import APIRouter, Path

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize
from app.audit.decorators import audit

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
    UserCreateRequest,
    UserCreateResponse,
    UserResponse,
    UserListResponse,
    UserUpdateRequest,
)
from . import service as auth_service


router = APIRouter()


@router.post("/challenge")
@audit()
async def get_login_challenge(
    req: ChallengeRequest, db: PostgresRunnerDep
) -> ChallengeResponse:
    return auth_service.create_login_challenge(req, db=db)


@router.post("/login")
@audit()
async def login_user(req: LoginRequest, db: PostgresRunnerDep) -> LoginResponse:
    return auth_service.login_user(req, db=db)


@router.post("/users")
@audit()
@authorize(AccessLevel.CONFIDENTIAL)
async def create_user(
    req: UserCreateRequest, db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UserCreateResponse:
    return auth_service.create_user(req, db=db)


@router.get("/users")
@audit()
@authorize(AccessLevel.CONFIDENTIAL)
async def read_users(
    db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> list[UserListResponse]:
    """Get simplified list of all users with only id and full name for admin purposes"""
    rows = db.query("""
        SELECT id, CONCAT(name, ' ', surname) as full_name
        FROM users
        ORDER BY surname, name, id
    """).many_rows()

    return [
        UserListResponse(
            id=row["id"],
            full_name=row["full_name"],
        )
        for row in rows
    ]


@router.get("/users/{id}")
@audit()
@authorize(AccessLevel.CONFIDENTIAL)
async def read_user(
    id: Annotated[int, Path()], db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UserResponse:
    return auth_service.get_user_by_id(id, db=db)


@router.put("/users/{id}")
@audit()
@authorize(AccessLevel.CONFIDENTIAL)
async def update_user(
    id: Annotated[int, Path()],
    req: UserUpdateRequest,
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
) -> UserResponse:
    return auth_service.update_user(id, req, db=db)
