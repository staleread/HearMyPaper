from fastapi.exceptions import HTTPException

from app.shared.utils.db import SqlRunner

from .models import User, UserCreateDto


def get_user_by_id(id: int, *, db: SqlRunner) -> User:
    row = (
        db.query("""
        SELECT id, username, access_level, categories, public_key
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
        access_level=row["access_level"],
        categories=set(row["categories"]),
        public_key=bytes(row["public_key"]),
    )


def create_user(dto: UserCreateDto, *, db: SqlRunner) -> int:
    return (
        db.query("""
            INSERT INTO users (username, access_level, categories, public_key)
            VALUES (:username, :access_level, :categories, :public_key)
            RETURNING id
        """)
        .bind(
            username=dto.username,
            access_level=dto.access_level,
            categories=list(dto.categories),
            public_key=dto.public_key,
        )
        .scalar(lambda x: int(x))
    )
