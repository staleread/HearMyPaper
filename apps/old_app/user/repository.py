from typing import Any
from hmp_core.storage import SqlRunner
from .dto import UserCreateRequest, UserUpdateRequest
from hmp_core.auth.pseudonyms import get_stable_pseudonym


def get_user_id_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> int | None:
    return (
        db.query("""
        SELECT id FROM users WHERE pseudonym = :pseudonym
    """)
        .bind(pseudonym=pseudonym)
        .scalar(lambda x: x)
    )


def get_public_key_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> bytes | None:
    return (
        db.query("""
        SELECT public_key FROM users WHERE pseudonym = :pseudonym
    """)
        .bind(pseudonym=pseudonym)
        .scalar(lambda x: x)
    )


def get_user_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> dict[str, Any] | None:
    return (
        db.query("""
        SELECT * FROM users WHERE pseudonym = :pseudonym
    """)
        .bind(pseudonym=pseudonym)
        .first_row()
    )


def create_user(
    req: UserCreateRequest, public_key_bytes: bytes, *, db: SqlRunner
) -> str:
    pseudonym = get_stable_pseudonym(req.email)
    db.query("""
        INSERT INTO users (pseudonym, name, surname, email, public_key, confidentiality_level, integrity_levels)
        VALUES (:pseudonym, :name, :surname, :email, :public_key, :conf_level, :integrity_levels)
    """).bind(
        pseudonym=pseudonym,
        name=req.name,
        surname=req.surname,
        email=req.email,
        public_key=public_key_bytes,
        conf_level=req.confidentiality_level.value,
        integrity_levels=[lvl.value for lvl in req.integrity_levels],
    ).execute()
    return pseudonym


def update_user_by_pseudonym(
    pseudonym: str, req: UserUpdateRequest, *, db: SqlRunner
) -> None:
    db.query("""
        UPDATE users 
        SET name = :name, 
            surname = :surname, 
            email = :email, 
            confidentiality_level = :conf_level, 
            integrity_levels = :integrity_levels
        WHERE pseudonym = :pseudonym
    """).bind(
        pseudonym=pseudonym,
        name=req.name,
        surname=req.surname,
        email=req.email,
        conf_level=req.confidentiality_level.value,
        integrity_levels=[lvl.value for lvl in req.integrity_levels],
    ).execute()
