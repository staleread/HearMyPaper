from typing import override
from sqlalchemy.ext.asyncio import AsyncSession

from shared_kernel.storage import SqlRunner
from identity_core.enums import AccessLevel
from identity_core.models import AuthUser
from identity_core.ports.outgoing.auth_repository import AuthRepositoryPort


class PostgresAuthRepositoryAdapter(AuthRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._sql = SqlRunner(session)

    @override
    async def get_user_by_id(self, id: str) -> AuthUser | None:
        row = (
            await self._sql.query(
                """
                SELECT id, public_key, confidentiality_level, integrity_levels
                FROM users
                WHERE id = :id
                """
            )
            .bind(id=id)
            .first_row()
        )

        if not row:
            return None

        return AuthUser(
            id=row["id"],
            public_key=row["public_key"],
            confidentiality_level=AccessLevel(row["confidentiality_level"]),
            integrity_levels=[AccessLevel(lvl) for lvl in row["integrity_levels"]],
        )
