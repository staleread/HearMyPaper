from app.shared.utils.db import SqlRunner

from . import repository as user_repo
from .models import UserDto, UserCreateDto


def get_user_by_id(id: int, *, db: SqlRunner) -> UserDto:
    user = user_repo.get_user_by_id(id, db=db)

    return UserDto(
        id=user.id,
        username=user.username,
        access_level=user.access_level,
        categories=list(user.categories),
        public_key=user.public_key,
    )


def add_user(dto: UserCreateDto, *, db: SqlRunner) -> int:
    return user_repo.create_user(dto, db=db)
