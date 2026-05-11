from httpx import AsyncClient
from uuid import UUID

from client_core.ports.outgoing.submissions import SubmissionsPort, SubmissionUploadInfo


class SubmissionsPortAdapter(SubmissionsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def request_upload_url(
        self, project_id: UUID, filename: str, extension: str
    ) -> SubmissionUploadInfo:
        payload = {
            "project_id": str(project_id),
            "filename": filename,
            "extension": extension,
        }
        response = await self.client.post("/submissions/upload-url", json=payload)
        response.raise_for_status()
        data = response.json()
        return SubmissionUploadInfo(
            url=data["upload_url"],
            submission_id=UUID(data["submission_id"]),
            filename=data["filename"],
            extension=data["extension"],
        )

    async def commit_submission(self, submission_id: UUID) -> None:
        response = await self.client.post(f"/submissions/{submission_id}/commit")
        response.raise_for_status()
