from pydantic import BaseModel, Field


class UploadKeyResponse(BaseModel):
    encrypted_aes_key: str


class PdfToAudioRequest(BaseModel):
    encrypted_file: str
    encrypted_aes_key: str
    speed: int = Field(default=140, ge=80, le=300)


class PdfToAudioResponse(BaseModel):
    encrypted_audio: str
    encrypted_audio_key: str
