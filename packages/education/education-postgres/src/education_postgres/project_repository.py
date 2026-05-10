from typing import override
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from education_core.models import Project, ProjectListItem
from education_core.ports.outgoing.project_repository import (
    ProjectRepositoryPort,
)


class PostgresProjectRepositoryAdapter(ProjectRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def get_projects_by_user_id(self, user_id: str) -> list[ProjectListItem]:
        result = await self._session.execute(
            text(
                """
                SELECT p.id, p.title, p.deadline
                FROM education.projects p
                LEFT JOIN education.project_students ps ON p.id = ps.project_id
                WHERE p.instructor_id = :user_id OR ps.student_id = :user_id
                ORDER BY p.deadline ASC
                """
            ),
            {"user_id": user_id},
        )
        rows = result.mappings().all()

        return [
            ProjectListItem(
                id=row["id"],
                title=row["title"],
                deadline=row["deadline"],
            )
            for row in rows
        ]

    @override
    async def get_by_id(self, project_id: UUID) -> Project | None:
        result = await self._session.execute(
            text(
                """
                SELECT id, title, description, instructor_id, deadline, created_at
                FROM education.projects
                WHERE id = :id
                """
            ),
            {"id": project_id},
        )
        row = result.mappings().first()

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

    @override
    async def exists_by_title(self, title: str) -> bool:
        result = await self._session.execute(
            text(
                "SELECT EXISTS(SELECT 1 FROM education.projects WHERE title = :title)"
            ),
            {"title": title},
        )
        return result.scalar() or False

    @override
    async def save(self, project: Project) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO education.projects (id, title, description, instructor_id, deadline, created_at, max_grade)
                VALUES (:id, :title, :description, :instructor_id, :deadline, :created_at, :max_grade)
                """
            ),
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "instructor_id": project.instructor_id,
                "deadline": project.deadline,
                "created_at": project.created_at,
                "max_grade": project.max_grade,
            },
        )

    @override
    async def update(self, project: Project) -> None:
        await self._session.execute(
            text(
                """
                UPDATE education.projects
                SET title = :title,
                    description = :description,
                    instructor_id = :instructor_id,
                    deadline = :deadline
                WHERE id = :id
                """
            ),
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "instructor_id": project.instructor_id,
                "deadline": project.deadline,
            },
        )
