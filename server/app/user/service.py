import base64
from fastapi.exceptions import HTTPException

from app.shared.utils.db import SqlRunner
from app.auth.service import get_access_by_role

from . import repository as user_repo
from .models import User
from .dto import UserResponse, UserCreateRequest, UserCreateResponse


def get_user_by_id(id: int, *, db: SqlRunner) -> UserResponse:
    user = user_repo.get_user_by_id(id, db=db)

    return UserResponse(
        id=user.id,
        username=user.username,
        confidentiality_level=user.confidentiality_level.value,
        integrity_levels=[level.value for level in user.integrity_levels],
        public_key=base64.b64encode(user.public_key).decode("utf-8"),
    )


def register_user(req: UserCreateRequest, *, db: SqlRunner) -> UserCreateResponse:
    existing_user = user_repo.find_user_by_username(req.username, db=db)

    if existing_user:
        raise HTTPException(
            status_code=400, detail=f"Username '{req.username}' is already taken"
        )

    confidentiality_level, integrity_levels = get_access_by_role(req.role)

    user = User(
        username=req.username,
        confidentiality_level=confidentiality_level,
        integrity_levels=integrity_levels,
        public_key=base64.b64decode(req.public_key),
    )

    id = user_repo.create_user(user, db=db)

    return UserCreateResponse(id=id)
