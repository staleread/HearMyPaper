from fastapi.exceptions import HTTPException

from app.auth.enums import AccessLevel
from app.shared.utils.db import SqlRunner

from .models import User


def get_user_by_id(id: int, *, db: SqlRunner) -> User:
    row = (
        db.query("""
        SELECT id, username, confidentiality_level, integrity_levels, public_key
        FROM users
        WHERE id = :id
    """)
        .bind(id=id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404, detail=f"User {id} not found")

    return User(
        id=row["id"],
        username=row["username"],
        confidentiality_level=AccessLevel(row["confidentiality_level"]),
        integrity_levels=[AccessLevel(level) for level in row["integrity_levels"]],
        public_key=bytes(row["public_key"]),
    )


def find_user_by_username(username: str, *, db: SqlRunner) -> User | None:
    row = (
        db.query("""
            SELECT id, username, confidentiality_level, integrity_levels, public_key
            FROM users
            WHERE username = :username
        """)
        .bind(username=username)
        .first_row()
    )

    if not row:
        return None

    return User(
        id=row["id"],
        username=row["username"],
        confidentiality_level=AccessLevel(row["confidentiality_level"]),
        integrity_levels=[AccessLevel(level) for level in row["integrity_levels"]],
        public_key=bytes(row["public_key"]),
    )


def create_user(user: User, *, db: SqlRunner) -> int:
    return (
        db.query("""
            INSERT INTO users (username, confidentiality_level, integrity_levels, public_key)
            VALUES (:username, :confidentiality_level, :integrity_levels, :public_key)
            RETURNING id
        """)
        .bind(
            username=user.username,
            confidentiality_level=user.confidentiality_level.value,
            integrity_levels=[level.value for level in user.integrity_levels],
            public_key=user.public_key,
        )
        .scalar(lambda x: int(x))
    )
