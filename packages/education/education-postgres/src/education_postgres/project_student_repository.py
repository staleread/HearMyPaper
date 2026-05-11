from typing import override
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from education_core.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)


class PostgresProjectStudentRepositoryAdapter(ProjectStudentRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def get_student_ids(self, project_id: UUID) -> list[str]:
        result = await self._session.execute(
            text(
                """
                SELECT student_id
                FROM education.project_students
                WHERE project_id = :project_id
                """
            ),
            {"project_id": project_id},
        )
        rows = result.mappings().all()
        return [row["student_id"] for row in rows]

    @override
    async def add_student(self, project_id: UUID, student_id: str) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO education.project_students (project_id, student_id)
                VALUES (:project_id, :student_id)
                """
            ),
            {"project_id": project_id, "student_id": student_id},
        )

    @override
    async def remove_student(self, project_id: UUID, student_id: str) -> None:
        await self._session.execute(
            text(
                """
                DELETE FROM education.project_students
                WHERE project_id = :project_id AND student_id = :student_id
                """
            ),
            {"project_id": project_id, "student_id": student_id},
        )

    @override
    async def is_student_assigned(self, project_id: UUID, student_id: str) -> bool:
        result = await self._session.execute(
            text(
                """
                SELECT COUNT(*)
                FROM education.project_students
                WHERE project_id = :project_id AND student_id = :student_id
                """
            ),
            {"project_id": project_id, "student_id": student_id},
        )
        count = result.scalar()
        return (count or 0) > 0
