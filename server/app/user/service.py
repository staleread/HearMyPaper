from sqlalchemy import Connection

from .models import User


def get_user_by_id(id: int, *, connection=Connection) -> User:
    return User(id=id, username="Nicolas")
