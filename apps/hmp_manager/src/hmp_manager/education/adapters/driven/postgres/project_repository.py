from typing import override
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hmp_core.storage import SqlRunner
from hmp_manager.education.domain.models import Project
from hmp_manager.education.domain.ports import ProjectRepository


class PostgresProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._sql = SqlRunner(session)

    @override
    async def get_projects_by_user_id(self, user_id: str) -> list[Project]:
        rows = (
            await self._sql.query(
                """
                SELECT p.id, p.title, p.description, p.instructor_id, p.deadline, p.created_at
                FROM projects p
                LEFT JOIN project_students ps ON p.id = ps.project_id
                WHERE p.instructor_id = :user_id OR ps.student_id = :user_id
                ORDER BY p.deadline ASC
                """
            )
            .bind(user_id=user_id)
            .many_rows()
        )

        return [
            Project(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                instructor_id=row["instructor_id"],
                deadline=row["deadline"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @override
    async def get_by_id(self, project_id: UUID) -> Project | None:
        row = (
            await self._sql.query(
                """
                SELECT id, title, description, instructor_id, deadline, created_at
                FROM projects
                WHERE id = :id
                """
            )
            .bind(id=project_id)
            .first_row()
        )

        if not row:
            return None

        return Project(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            instructor_id=row["instructor_id"],
            deadline=row["deadline"],
            created_at=row["created_at"],
        )
