from result import Result, Err

from .dto import UploadKeyResponse, PdfToAudioRequest, PdfToAudioResponse
from ..shared.utils.api import check_response
from ..shared.utils.session import ApiSession


def get_upload_key(session: ApiSession) -> Result[UploadKeyResponse, str]:
    try:
        r = session.get("/pdf-to-audio/upload-key")
        result = check_response(r)
        return result.map(lambda data: UploadKeyResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def execute_pdf_to_audio(
    session: ApiSession, req: PdfToAudioRequest
) -> Result[PdfToAudioResponse, str]:
    try:
        r = session.post("/pdf-to-audio/execute", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: PdfToAudioResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")
