from typing import Annotated
from fastapi import APIRouter, Path

from app.shared.dependencies.db import PostgresRunnerDep

from .models import UserDto
from . import service as user_service

router = APIRouter()


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: Annotated[int, Path()], db: PostgresRunnerDep
) -> UserDto:
    return user_service.get_user_by_id(user_id, db=db)
