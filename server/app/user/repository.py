from fastapi.exceptions import HTTPException

from app.auth.models import AccessRule
from app.auth.enums import AccessLevel
from app.shared.utils.db import SqlRunner

from .models import User


def get_user_by_id(id: int, *, db: SqlRunner) -> User:
    row = (
        db.query("""
        SELECT id, username, access_level, access_rules, public_key
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
        access_level=AccessLevel(row["access_level"]),
        access_rules=[AccessRule.parse(rule) for rule in row["access_rules"]],
        public_key=bytes(row["public_key"]),
    )


def find_user_by_username(username: str, *, db: SqlRunner) -> User | None:
    row = (
        db.query("""
            SELECT id, username, access_level, access_rules, public_key
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
        access_level=row["access_level"],
        access_rules=[AccessRule.parse(rule) for rule in row["access_rules"]],
        public_key=bytes(row["public_key"]),
    )


def create_user(user: User, *, db: SqlRunner) -> int:
    return (
        db.query("""
            INSERT INTO users (username, access_level, access_rules, public_key)
            VALUES (:username, :access_level, :access_rules, :public_key)
            RETURNING id
        """)
        .bind(
            username=user.username,
            access_level=user.access_level.value,
            access_rules=user.access_rules,
            public_key=user.public_key,
        )
        .scalar(lambda x: int(x))
    )
