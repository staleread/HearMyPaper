from pydantic import BaseModel
from uuid import UUID


class SubmissionIntentRequest(BaseModel):
    project_id: int
    filename: str
    content_hash: str


class SubmissionIntentResponse(BaseModel):
    upload_url: str
    submission_uuid: UUID
