from typing import override
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from processing_core.models import Conversion, ConversionStatus
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)


class PostgresConversionRepositoryAdapter(ConversionRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def save_conversion(self, conversion: Conversion) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO processing.conversions (
                    conversion_id, lab_attempt_id, instructor_id, worker_id, status, created_at, updated_at
                ) VALUES (
                    :conversion_id, :lab_attempt_id, :instructor_id, :worker_id, :status, :created_at, :updated_at
                )
                """
            ),
            {
                "conversion_id": conversion.conversion_id,
                "lab_attempt_id": conversion.lab_attempt_id,
                "instructor_id": conversion.instructor_id,
                "worker_id": conversion.worker_id,
                "status": conversion.status.value,
                "created_at": conversion.created_at,
                "updated_at": conversion.updated_at,
            },
        )

    @override
    async def get_conversion(self, conversion_id: UUID) -> Conversion | None:
        result = await self._session.execute(
            text(
                """
                SELECT conversion_id, lab_attempt_id, instructor_id, worker_id, status, created_at, updated_at
                FROM processing.conversions
                WHERE conversion_id = :id
                """
            ),
            {"id": conversion_id},
        )
        row = result.mappings().first()
        if not row:
            return None
        return Conversion(
            conversion_id=row["conversion_id"],
            lab_attempt_id=row["lab_attempt_id"],
            instructor_id=row["instructor_id"],
            worker_id=row["worker_id"],
            status=ConversionStatus(row["status"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @override
    async def update_status(self, conversion_id: UUID, status: str) -> None:
        await self._session.execute(
            text(
                """
                UPDATE processing.conversions
                SET status = :status, updated_at = NOW()
                WHERE conversion_id = :id
                """
            ),
            {"id": conversion_id, "status": status},
        )
