from pydantic import BaseModel


class SubmissionResponse(BaseModel):
    id: int
    title: str
    student_name: str
    instructor_name: str
    submitted_at: str
    content_hash: str


class SubmissionHashResponse(BaseModel):
    content_hash: str


class UploadKeyResponse(BaseModel):
    encrypted_aes_key: str


class PdfToAudioRequest(BaseModel):
    encrypted_file: str
    encrypted_aes_key: str
    speed: int = 140


class PdfToAudioResponse(BaseModel):
    encrypted_audio: str
    encrypted_audio_key: str
