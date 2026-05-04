from uuid import UUID

from pydantic import BaseModel, Field

from hmp_core.auth.enums import AccessLevel


class ConversionJobTask(BaseModel):
    job_id: UUID
    # The 'Subject' properties for BLP checks in the worker
    subject_pseudonym: str
    recipient_pseudonym: str
    confidentiality_level: AccessLevel

    # Path to the encrypted PDF in MinIO
    input_object_path: str  # e.g., "uploads/user-123/file.enc.pdf"

    # Metadata for the TTS engine
    language: str = "en-US"
    priority: int = Field(default=1, ge=1, le=5)
    speed: int = Field(default=140, ge=80, le=300)

    correlation_id: str  # To track the request across services
