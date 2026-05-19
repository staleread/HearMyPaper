from typing import override
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from identity_core.enums import AccessLevel
from identity_core.models import AuthUser
from identity_core.ports.outgoing.auth_repository import AuthRepositoryPort


class PostgresAuthRepositoryAdapter(AuthRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def get_user_by_id(self, id: str) -> AuthUser | None:
        result = await self._session.execute(
            text(
                """
                SELECT id, confidentiality_level, integrity_levels
                FROM identity.users
                WHERE id = :id
                """
            ),
            {"id": id},
        )
        row = result.mappings().first()

        if not row:
            return None

        return AuthUser(
            id=row["id"],
            confidentiality_level=AccessLevel(row["confidentiality_level"]),
            integrity_levels=[AccessLevel(lvl) for lvl in row["integrity_levels"]],
        )
