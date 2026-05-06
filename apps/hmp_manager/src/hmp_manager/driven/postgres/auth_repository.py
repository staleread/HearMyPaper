from typing import override
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.storage import SqlRunner
from hmp_manager.domain.auth.models import AuthUser, AccessLevel
from hmp_manager.domain.auth.ports import AuthRepository


class PostgresAuthRepository(AuthRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._sql = SqlRunner(session)

    @override
    async def get_user_by_pseudonym(self, pseudonym: str) -> AuthUser | None:
        row = (
            await self._sql.query(
                """
                SELECT pseudonym, public_key, confidentiality_level, integrity_levels
                FROM users
                WHERE pseudonym = :pseudonym
                """
            )
            .bind(pseudonym=pseudonym)
            .first_row()
        )

        if not row:
            return None

        return AuthUser(
            pseudonym=row["pseudonym"],
            public_key=row["public_key"],
            confidentiality_level=AccessLevel(row["confidentiality_level"]),
            integrity_levels=[AccessLevel(lvl) for lvl in row["integrity_levels"]],
        )
