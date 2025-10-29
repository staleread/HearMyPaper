import base64
from result import Result, Err, Ok
from pydantic import TypeAdapter

from .dto import UploadKeyResponse, PdfToAudioRequest, PdfToAudioResponse
from ..shared.utils.api import check_response
from ..shared.utils.session import ApiSession


def get_server_public_key(session: ApiSession) -> Result[bytes, str]:
    try:
        r = session.get("/public-key")
        result = check_response(r)

        def decode_key(data: dict | bytes) -> Result[bytes, str]:
            if isinstance(data, dict):
                return Ok(base64.b64decode(data["public_key"]))
            return Err("Unexpected response format")

        return result.and_then(decode_key)
    except Exception as e:
        return Err(f"Network error: {e}")


def get_upload_key(session: ApiSession) -> Result[UploadKeyResponse, str]:
    try:
        r = session.get("/pdf-to-audio/upload-key")
        result = check_response(r)
        return result.map(
            lambda data: TypeAdapter(UploadKeyResponse).validate_python(data)
        )
    except Exception as e:
        return Err(f"Network error: {e}")


def execute_pdf_to_audio(
    session: ApiSession, req: PdfToAudioRequest
) -> Result[PdfToAudioResponse, str]:
    try:
        r = session.post("/pdf-to-audio/execute", json=req.model_dump())
        result = check_response(r)
        return result.map(
            lambda data: TypeAdapter(PdfToAudioResponse).validate_python(data)
        )
    except Exception as e:
        return Err(f"Network error: {e}")
