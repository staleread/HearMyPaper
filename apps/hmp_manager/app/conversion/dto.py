from uuid import UUID
from pydantic import BaseModel

class ConversionIntentRequest(BaseModel):
    submission_id: int
    filename: str

class ConversionIntentResponse(BaseModel):
    upload_url: str
    conversion_uuid: UUID
