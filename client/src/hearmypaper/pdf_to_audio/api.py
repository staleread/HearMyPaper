import requests
from result import Result, Err

from .dto import UploadKeyResponse, PdfToAudioRequest, PdfToAudioResponse
from ..shared.utils.api import check_response


def get_upload_key(session: requests.Session) -> Result[UploadKeyResponse, str]:
    """Get AES key for encrypting PDF file"""
    try:
        r = session.get("https://localhost/pdf-to-audio/upload-key")
        result = check_response(r)
        return result.map(lambda data: UploadKeyResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def execute_pdf_to_audio(
    session: requests.Session, req: PdfToAudioRequest
) -> Result[PdfToAudioResponse, str]:
    """Send encrypted PDF and get encrypted audio back"""
    try:
        r = session.post(
            "https://localhost/pdf-to-audio/execute", json=req.model_dump()
        )
        result = check_response(r)
        return result.map(lambda data: PdfToAudioResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")
