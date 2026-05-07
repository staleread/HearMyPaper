from typing import override
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.storage import SqlRunner
from hmp_manager.identity.domain.enums import AccessLevel
from hmp_manager.identity.domain.models import AuthUser
from hmp_manager.identity.domain.ports.outgoing import AuthRepositoryPort


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
