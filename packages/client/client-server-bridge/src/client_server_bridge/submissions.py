from httpx import AsyncClient
from uuid import UUID

from client_core.ports.outgoing.submissions import SubmissionsPort


class SubmissionsPortAdapter(SubmissionsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def request_upload_url(
        self, project_id: UUID, file_extension: str
    ) -> tuple[str, UUID]:
        payload = {
            "project_id": str(project_id),
            "file_extension": file_extension,
        }
        response = await self.client.post("/submissions/upload-url", json=payload)
        response.raise_for_status()
        data = response.json()
        return data["upload_url"], UUID(data["submission_id"])

    async def commit_submission(self, submission_id: UUID) -> None:
        response = await self.client.post(f"/submissions/{submission_id}/commit")
        response.raise_for_status()
