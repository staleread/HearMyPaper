import json
from typing import override
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from submissions_core.models import LabSubmission, SubmissionStatus, SubmissionListItem
from submissions_core.ports.outgoing.submission_repository import (
    SubmissionRepositoryPort,
)


class PostgresSubmissionRepositoryAdapter(SubmissionRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def save(self, submission: LabSubmission) -> None:
        await self._session.execute(
            text(
                """
                INSERT INTO submissions.submissions (
                    submission_id, student_id, project_id, storage_path, status, created_at, filename, extension, metadata
                ) VALUES (
                    :submission_id, :student_id, :project_id, :storage_path, :status, :created_at, :filename, :extension, :metadata
                )
                """
            ),
            {
                "submission_id": submission.submission_id,
                "student_id": submission.student_id,
                "project_id": submission.project_id,
                "storage_path": submission.storage_path,
                "status": submission.status.value,
                "created_at": submission.created_at,
                "filename": submission.filename,
                "extension": submission.extension,
                "metadata": json.dumps(submission.metadata),
            },
        )

    @override
    async def find_by_id(self, submission_id: UUID) -> LabSubmission | None:
        result = await self._session.execute(
            text(
                """
                SELECT submission_id, student_id, project_id, storage_path, status, created_at, filename, extension, metadata
                FROM submissions.submissions
                WHERE submission_id = :submission_id
                """
            ),
            {"submission_id": submission_id},
        )
        row = result.mappings().first()
        if not row:
            return None

        return LabSubmission(
            submission_id=row["submission_id"],
            student_id=row["student_id"],
            project_id=row["project_id"],
            storage_path=row["storage_path"],
            status=SubmissionStatus(row["status"]),
            created_at=row["created_at"],
            filename=row["filename"],
            extension=row["extension"],
            metadata=row["metadata"]
            if isinstance(row["metadata"], dict)
            else json.loads(row["metadata"]),
        )

    @override
    async def find_by_student_and_project(
        self, student_id: str, project_id: UUID
    ) -> LabSubmission | None:
        result = await self._session.execute(
            text(
                """
                SELECT submission_id, student_id, project_id, storage_path, status, created_at, filename, extension, metadata
                FROM submissions.submissions
                WHERE student_id = :student_id AND project_id = :project_id
                """
            ),
            {"student_id": student_id, "project_id": project_id},
        )
        row = result.mappings().first()
        if not row:
            return None

        return LabSubmission(
            submission_id=row["submission_id"],
            student_id=row["student_id"],
            project_id=row["project_id"],
            storage_path=row["storage_path"],
            status=SubmissionStatus(row["status"]),
            created_at=row["created_at"],
            filename=row["filename"],
            extension=row["extension"],
            metadata=row["metadata"]
            if isinstance(row["metadata"], dict)
            else json.loads(row["metadata"]),
        )

    @override
    async def list_by_project(self, project_id: UUID) -> list[SubmissionListItem]:
        result = await self._session.execute(
            text(
                """
                SELECT submission_id, student_id, status, created_at
                FROM submissions.submissions
                WHERE project_id = :project_id
                ORDER BY created_at DESC
                """
            ),
            {"project_id": project_id},
        )
        rows = result.mappings().all()

        return [
            SubmissionListItem(
                submission_id=row["submission_id"],
                student_id=row["student_id"],
                status=SubmissionStatus(row["status"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @override
    async def update_status(
        self, submission_id: UUID, status: SubmissionStatus
    ) -> None:
        await self._session.execute(
            text(
                """
                UPDATE submissions.submissions
                SET status = :status
                WHERE submission_id = :submission_id
                """
            ),
            {"submission_id": submission_id, "status": status.value},
        )
