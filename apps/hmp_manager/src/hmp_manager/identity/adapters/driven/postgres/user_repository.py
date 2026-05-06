from typing import override
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.storage import SqlRunner
from hmp_manager.identity.domain.models import User, UserUpdate
from hmp_manager.identity.domain.ports import UserRepository
from hmp_manager.identity.domain.enums import AccessLevel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._sql = SqlRunner(session)

    @override
    async def save(self, user: User, public_key: bytes) -> None:
        await (
            self._sql.query(
                """
            INSERT INTO users (id, name, surname, email, public_key, confidentiality_level, integrity_levels, created_at)
            VALUES (:id, :name, :surname, :email, :public_key, :conf_level, :integrity_levels, :created_at)
            """
            )
            .bind(
                id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                public_key=public_key,
                conf_level=user.confidentiality_level.value,
                integrity_levels=[lvl.value for lvl in user.integrity_levels],
                created_at=user.created_at,
            )
            .execute()
        )

    @override
    async def get_by_id(self, id: str) -> User | None:
        row = (
            await self._sql.query(
                """
                SELECT id, name, surname, email, confidentiality_level, integrity_levels, created_at
                FROM users
                WHERE id = :id
                """
            )
            .bind(id=id)
            .first_row()
        )

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
    async def get_by_email(self, email: str) -> User | None:
        row = (
            await self._sql.query(
                """
                SELECT id, name, surname, email, confidentiality_level, integrity_levels, created_at
                FROM users
                WHERE email = :email
                """
            )
            .bind(email=email)
            .first_row()
        )

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
        return (
            await self._sql.query("SELECT public_key FROM users WHERE id = :id")
            .bind(id=id)
            .scalar(bytes)
        )

    @override
    async def update(self, id: str, user_update: UserUpdate) -> User:
        await (
            self._sql.query(
                """
            UPDATE users
            SET name = :name,
                surname = :surname,
                email = :email,
                confidentiality_level = :conf_level,
                integrity_levels = :integrity_levels
            WHERE id = :id
            """
            )
            .bind(
                id=id,
                name=user_update.name,
                surname=user_update.surname,
                email=user_update.email,
                conf_level=user_update.confidentiality_level.value,
                integrity_levels=[lvl.value for lvl in user_update.integrity_levels],
            )
            .execute()
        )

        user = await self.get_by_id(id)
        if not user:
            raise RuntimeError(f"User with id {id} disappeared after update")
        return user

    @override
    async def exists_with_email(self, email: str) -> bool:
        count = (
            await self._sql.query("SELECT COUNT(*) FROM users WHERE email = :email")
            .bind(email=email)
            .scalar(int)
        )
        return count > 0
