from uuid import UUID

import httpx

from .dto import SubmissionIntentRequest, SubmissionIntentResponse


async def post_submission_intent(
    client: httpx.AsyncClient, base_url: str, req: SubmissionIntentRequest
) -> SubmissionIntentResponse:
    """Declares intent to submit an encrypted PDF."""
    response = await client.post(f"{base_url}/submission/intent", json=req.model_dump())
    response.raise_for_status()
    return SubmissionIntentResponse.model_validate(response.json())


async def commit_submission(
    client: httpx.AsyncClient, base_url: str, submission_uuid: UUID
) -> None:
    """Finalizes a submission after the client has uploaded the file."""
    response = await client.post(f"{base_url}/submission/{submission_uuid}/commit")
    response.raise_for_status()
