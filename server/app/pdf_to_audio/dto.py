from pydantic import BaseModel


class UploadKeyResponse(BaseModel):
    encrypted_aes_key: str


class PdfToAudioRequest(BaseModel):
    encrypted_file: str
    encrypted_aes_key: str


class PdfToAudioResponse(BaseModel):
    encrypted_audio: str
    encrypted_audio_key: str
