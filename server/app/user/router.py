from typing import Annotated
from fastapi import APIRouter, Path

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize

from .dto import UserResponse, UserCreateRequest, UserCreateResponse
from . import service as user_service

router = APIRouter()


@router.get("/me")
@authorize(AccessLevel.UNCLASSIFIED)
async def read_my_user(
    db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UserResponse:
    return user_service.get_user_by_id(subject.id, db=db)


@router.get("/{id}")
@authorize(AccessLevel.CONTROLLED)
async def read_user(
    id: Annotated[int, Path()], db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UserResponse:
    return user_service.get_user_by_id(id, db=db)


@router.post("/register")
@authorize(AccessLevel.CONTROLLED)
async def create_user(
    req: UserCreateRequest, db: PostgresRunnerDep, subject: CurrentSubjectDep
) -> UserCreateResponse:
    return user_service.register_user(req, db=db)
