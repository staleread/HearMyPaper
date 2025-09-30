from fastapi.exceptions import HTTPException

from app.auth.enums import AccessLevel
from app.shared.utils.db import SqlRunner

from .models import User


def get_user_by_id(id: int, *, db: SqlRunner) -> User:
    row = (
        db.query(
            "SELECT id, name, surname, email, confidentiality_level, integrity_levels, public_key, expires_at FROM users WHERE id = :id"
        )
        .bind(id=id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404, detail=f"User {id} not found")

    return User(
        id=row["id"],
        name=row["name"],
        surname=row["surname"],
        email=row["email"],
        confidentiality_level=AccessLevel(row["confidentiality_level"]),
        integrity_levels=[AccessLevel(level) for level in row["integrity_levels"]],
        public_key=bytes(row["public_key"]),
        expires_at=row["expires_at"].isoformat(),
    )


def user_exists_by_name_surname(
    name: str, surname: str, *, exclude_user_id: int | None = None, db: SqlRunner
) -> bool:
    """Check if user exists by name and surname combination, optionally excluding a specific user ID (for updates)"""
    if exclude_user_id is not None:
        return (
            db.query(
                "SELECT 1 FROM users WHERE name = :name AND surname = :surname AND id != :exclude_user_id"
            )
            .bind(name=name, surname=surname, exclude_user_id=exclude_user_id)
            .scalar(lambda x: x is not None)
        )
    else:
        return (
            db.query("SELECT 1 FROM users WHERE name = :name AND surname = :surname")
            .bind(name=name, surname=surname)
            .scalar(lambda x: x is not None)
        )


def user_exists_by_email(
    email: str, *, exclude_user_id: int | None = None, db: SqlRunner
) -> bool:
    """Check if user exists by email, optionally excluding a specific user ID (for updates)"""
    if exclude_user_id is not None:
        return (
            db.query(
                "SELECT 1 FROM users WHERE email = :email AND id != :exclude_user_id"
            )
            .bind(email=email, exclude_user_id=exclude_user_id)
            .scalar(lambda x: x is not None)
        )
    else:
        return (
            db.query("SELECT 1 FROM users WHERE email = :email")
            .bind(email=email)
            .scalar(lambda x: x is not None)
        )


def create_user(user: User, *, db: SqlRunner) -> int:
    # Check for duplicate name/surname combination
    if user_exists_by_name_surname(user.name, user.surname, db=db):
        raise HTTPException(
            status_code=400,
            detail=f"User with name '{user.name} {user.surname}' already exists",
        )

    # Check for duplicate email
    if user_exists_by_email(user.email, db=db):
        raise HTTPException(
            status_code=400, detail=f"Email '{user.email}' is already taken"
        )

    return (
        db.query(
            "INSERT INTO users (name, surname, email, confidentiality_level, integrity_levels, public_key, expires_at) VALUES (:name, :surname, :email, :confidentiality_level, :integrity_levels, :public_key, :expires_at) RETURNING id"
        )
        .bind(
            name=user.name,
            surname=user.surname,
            email=user.email,
            confidentiality_level=user.confidentiality_level.value,
            integrity_levels=[level.value for level in user.integrity_levels],
            public_key=user.public_key,
            expires_at=user.expires_at,
        )
        .scalar(lambda x: int(x))
    )


def update_user(user: User, *, db: SqlRunner) -> None:
    # First verify the user exists
    get_user_by_id(user.id, db=db)

    # Check for duplicate name/surname combination (excluding current user)
    if user_exists_by_name_surname(
        user.name, user.surname, exclude_user_id=user.id, db=db
    ):
        raise HTTPException(
            status_code=400,
            detail=f"User with name '{user.name} {user.surname}' already exists",
        )

    # Check for duplicate email (excluding current user)
    if user_exists_by_email(user.email, exclude_user_id=user.id, db=db):
        raise HTTPException(
            status_code=400, detail=f"Email '{user.email}' is already taken"
        )

    # Execute the update (excluding public_key which should not be updatable)
    (
        db.query(
            "UPDATE users SET name = :name, surname = :surname, email = :email, confidentiality_level = :confidentiality_level, integrity_levels = :integrity_levels, expires_at = :expires_at WHERE id = :id"
        )
        .bind(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            confidentiality_level=user.confidentiality_level.value,
            integrity_levels=[level.value for level in user.integrity_levels],
            expires_at=user.expires_at,
        )
        .execute()
    )
