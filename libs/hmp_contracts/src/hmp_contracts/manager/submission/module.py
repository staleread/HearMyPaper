from uuid import UUID

import httpx

from .dto import SubmissionIntentRequest, SubmissionIntentResponse


class SubmissionModule:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def post_intent(
        self, req: SubmissionIntentRequest
    ) -> SubmissionIntentResponse:
        """Declares intent to submit an encrypted PDF."""
        response = await self.client.post("/submission/intent", json=req.model_dump())
        response.raise_for_status()
        return SubmissionIntentResponse.model_validate(response.json())

    async def commit(self, submission_uuid: UUID) -> None:
        """Finalizes a submission after the client has uploaded the file."""
        response = await self.client.post(f"/submission/{submission_uuid}/commit")
        response.raise_for_status()
