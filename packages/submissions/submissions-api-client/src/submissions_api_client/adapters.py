from httpx import AsyncClient
from datetime import datetime
from uuid import UUID
from typing import override

from submissions_core.models import LabSubmission, SubmissionListItem, SubmissionStatus
from submissions_core.ports.incoming import (
    RequestUploadUrlPort,
    CommitSubmissionPort,
    GetSubmissionPort,
    ListProjectSubmissionsPort,
    RequestSubmissionUploadCommand,
    CommitSubmissionCommand,
)


class RequestUploadUrlAdapter(RequestUploadUrlPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: RequestSubmissionUploadCommand) -> str:
        payload = {
            "project_id": str(cmd.project_id),
            "file_extension": cmd.file_extension,
        }
        response = await self.client.post("/submissions/upload-url", json=payload)
        response.raise_for_status()
        return response.json()["upload_url"]


class CommitSubmissionAdapter(CommitSubmissionPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: CommitSubmissionCommand) -> None:
        response = await self.client.post(f"/submissions/{cmd.submission_id}/commit")
        response.raise_for_status()


class GetSubmissionAdapter(GetSubmissionPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, submission_id: UUID) -> LabSubmission:
        response = await self.client.get(f"/submissions/{submission_id}")
        response.raise_for_status()
        s = response.json()
        return LabSubmission(
            submission_id=UUID(s["submission_id"]),
            student_id=s["student_id"],
            project_id=UUID(s["project_id"]),
            storage_path=s["storage_path"],
            status=SubmissionStatus(s["status"]),
            created_at=datetime.fromisoformat(s["created_at"]),
            metadata=s["metadata"],
        )


class ListProjectSubmissionsAdapter(ListProjectSubmissionsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, project_id: UUID) -> list[SubmissionListItem]:
        response = await self.client.get(f"/submissions/project/{project_id}")
        response.raise_for_status()
        data = response.json()
        return [
            SubmissionListItem(
                submission_id=UUID(s["submission_id"]),
                student_id=s["student_id"],
                status=SubmissionStatus(s["status"]),
                created_at=datetime.fromisoformat(s["created_at"]),
            )
            for s in data
        ]
