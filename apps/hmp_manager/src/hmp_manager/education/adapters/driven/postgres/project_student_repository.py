from typing import override
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.storage import SqlRunner
from hmp_manager.education.domain.ports import ProjectStudentRepository


class PostgresProjectStudentRepository(ProjectStudentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._sql = SqlRunner(session)

    @override
    async def get_student_ids(self, project_id: UUID) -> list[str]:
        rows = (
            await self._sql.query(
                """
                SELECT student_id
                FROM project_students
                WHERE project_id = :project_id
                """
            )
            .bind(project_id=project_id)
            .many_rows()
        )
        return [row["student_id"] for row in rows]

    @override
    async def add_student(self, project_id: UUID, student_id: str) -> None:
        await (
            self._sql.query(
                """
                INSERT INTO project_students (project_id, student_id)
                VALUES (:project_id, :student_id)
                """
            )
            .bind(project_id=project_id, student_id=student_id)
            .execute()
        )

    @override
    async def remove_student(self, project_id: UUID, student_id: str) -> None:
        await (
            self._sql.query(
                """
                DELETE FROM project_students
                WHERE project_id = :project_id AND student_id = :student_id
                """
            )
            .bind(project_id=project_id, student_id=student_id)
            .execute()
        )

    @override
    async def is_student_assigned(self, project_id: UUID, student_id: str) -> bool:
        count = (
            await self._sql.query(
                """
                SELECT COUNT(*)
                FROM project_students
                WHERE project_id = :project_id AND student_id = :student_id
                """
            )
            .bind(project_id=project_id, student_id=student_id)
            .scalar(int)
        )
        return count > 0
