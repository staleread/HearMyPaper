from typing import Annotated
from fastapi import APIRouter, Path

from app.shared.dependencies.db import PostgresRunnerDep

from .dto import UserResponse, UserCreateRequest, UserCreateResponse
from . import service as user_service

router = APIRouter()


@router.get("/{id}")
async def get_user_by_id(
    id: Annotated[int, Path()], db: PostgresRunnerDep
) -> UserResponse:
    return user_service.get_user_by_id(id, db=db)


@router.post("/register")
async def register_user(
    req: UserCreateRequest, db: PostgresRunnerDep
) -> UserCreateResponse:
    return user_service.register_user(req, db=db)
