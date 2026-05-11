from typing import override
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from identity_core.models import User
from identity_core.ports.outgoing.user_repository import (
    UserRepositoryPort,
    UserUpdateCommand,
)
from identity_core.enums import AccessLevel


class PostgresUserRepositoryAdapter(UserRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def save(self, user: User, public_key: bytes) -> None:
        await self._session.execute(
            text(
                """
            INSERT INTO identity.users (id, name, surname, email, public_key, confidentiality_level, integrity_levels, created_at)
            VALUES (:id, :name, :surname, :email, :public_key, :conf_level, :integrity_levels, :created_at)
            """
            ),
            {
                "id": user.id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "public_key": public_key,
                "conf_level": user.confidentiality_level.value,
                "integrity_levels": [lvl.value for lvl in user.integrity_levels],
                "created_at": user.created_at,
            },
        )

    @override
    async def get_by_id(self, id: str) -> User | None:
        result = await self._session.execute(
            text(
                """
                SELECT id, name, surname, email, confidentiality_level, integrity_levels, created_at
                FROM identity.users
                WHERE id = :id
                """
            ),
            {"id": id},
        )
        row = result.mappings().first()

        if not row:
            return None

        return User(
            id=row["id"],
            name=row["name"],
            surname=row["surname"],
            email=row["email"],
            confidentiality_level=AccessLevel(row["confidentiality_level"]),
            integrity_levels=[AccessLevel(lvl) for lvl in row["integrity_levels"]],
            created_at=row["created_at"],
        )

    @override
    async def get_public_key_by_id(self, id: str) -> bytes | None:
        result = await self._session.execute(
            text("SELECT public_key FROM identity.users WHERE id = :id"), {"id": id}
        )
        return result.scalar()

    @override
    async def update(self, id: str, user_update: UserUpdateCommand) -> User:
        await self._session.execute(
            text(
                """
            UPDATE identity.users
            SET name = :name,
                surname = :surname,
                email = :email,
                confidentiality_level = :conf_level,
                integrity_levels = :integrity_levels
            WHERE id = :id
            """
            ),
            {
                "id": id,
                "name": user_update.name,
                "surname": user_update.surname,
                "email": user_update.email,
                "conf_level": user_update.confidentiality_level.value,
                "integrity_levels": [lvl.value for lvl in user_update.integrity_levels],
            },
        )

        user = await self.get_by_id(id)
        if not user:
            raise RuntimeError(f"User with id {id} disappeared after update")
        return user

    @override
    async def exists_with_email(self, email: str) -> bool:
        result = await self._session.execute(
            text("SELECT COUNT(*) FROM identity.users WHERE email = :email"),
            {"email": email},
        )
        count = result.scalar()
        return (count or 0) > 0

    @override
    async def has_any_users(self) -> bool:
        result = await self._session.execute(
            text("SELECT EXISTS(SELECT 1 FROM identity.users)")
        )
        return result.scalar() or False
