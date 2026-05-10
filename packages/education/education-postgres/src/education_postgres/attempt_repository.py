from typing import override
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from education_core.models import LabAttempt, AttemptListItem
from education_core.ports.outgoing.attempt_repository import AttemptRepositoryPort


class PostgresAttemptRepositoryAdapter(AttemptRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def save(self, attempt: LabAttempt) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO education.lab_attempts (
                    attempt_id, student_id, project_id, submission_id, 
                    submitted_at, is_on_time, grade, instructor_feedback
                )
                VALUES (
                    :attempt_id, :student_id, :project_id, :submission_id, 
                    :submitted_at, :is_on_time, :grade, :instructor_feedback
                )
                """
            ),
            {
                "attempt_id": attempt.attempt_id,
                "student_id": attempt.student_id,
                "project_id": attempt.project_id,
                "submission_id": attempt.submission_id,
                "submitted_at": attempt.submitted_at,
                "is_on_time": attempt.is_on_time,
                "grade": attempt.grade,
                "instructor_feedback": attempt.instructor_feedback,
            },
        )

    @override
    async def find_by_student_and_project(
        self, student_id: str, project_id: UUID
    ) -> LabAttempt | None:
        result = await self._session.execute(
            text(
                """
                SELECT 
                    attempt_id, student_id, project_id, submission_id, 
                    submitted_at, is_on_time, grade, instructor_feedback
                FROM education.lab_attempts
                WHERE student_id = :student_id AND project_id = :project_id
                """
            ),
            {"student_id": student_id, "project_id": project_id},
        )
        row = result.mappings().first()

        if not row:
            return None

        return LabAttempt(
            attempt_id=row["attempt_id"],
            student_id=row["student_id"],
            project_id=row["project_id"],
            submission_id=row["submission_id"],
            submitted_at=row["submitted_at"],
            is_on_time=row["is_on_time"],
            grade=row["grade"],
            instructor_feedback=row["instructor_feedback"],
        )

    @override
    async def get_by_submission_id(self, submission_id: UUID) -> LabAttempt | None:
        result = await self._session.execute(
            text(
                """
                SELECT 
                    attempt_id, student_id, project_id, submission_id, 
                    submitted_at, is_on_time, grade, instructor_feedback
                FROM education.lab_attempts
                WHERE submission_id = :submission_id
                """
            ),
            {"submission_id": submission_id},
        )
        row = result.mappings().first()

        if not row:
            return None

        return LabAttempt(
            attempt_id=row["attempt_id"],
            student_id=row["student_id"],
            project_id=row["project_id"],
            submission_id=row["submission_id"],
            submitted_at=row["submitted_at"],
            is_on_time=row["is_on_time"],
            grade=row["grade"],
            instructor_feedback=row["instructor_feedback"],
        )

    @override
    async def find_by_project(self, project_id: UUID) -> list[AttemptListItem]:
        result = await self._session.execute(
            text(
                """
                SELECT 
                    attempt_id, student_id, submitted_at, is_on_time, grade
                FROM education.lab_attempts
                WHERE project_id = :project_id
                ORDER BY submitted_at DESC
                """
            ),
            {"project_id": project_id},
        )
        rows = result.mappings().all()

        return [
            AttemptListItem(
                attempt_id=row["attempt_id"],
                student_id=row["student_id"],
                submitted_at=row["submitted_at"],
                is_on_time=row["is_on_time"],
                grade=row["grade"],
            )
            for row in rows
        ]
