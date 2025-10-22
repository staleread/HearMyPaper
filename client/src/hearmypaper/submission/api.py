import cbor2
from result import Result

from ..shared.utils import api as api_utils
from ..shared.utils.session import ApiSession
from . import dto


def list_submissions(session: ApiSession) -> Result[list[dto.SubmissionResponse], str]:
    response = session.get("/submission")
    result = api_utils.check_response(response)

    if result.is_err():
        return result

    result.unwrap()
    return result.map(lambda d: [dto.SubmissionResponse(**item) for item in d])


def upload_submission(
    session: ApiSession, project_id: int, title: str, encrypted_content: bytes
) -> Result[int, str]:
    payload = {
        "project_id": project_id,
        "title": title,
        "encrypted_content": encrypted_content,
    }
    cbor_bytes = cbor2.dumps(payload)

    response = session.post(
        "/submission",
        headers={"Content-Type": "application/cbor"},
        data=cbor_bytes,
    )

    result = api_utils.check_response(response)
    return result.map(lambda d: d["id"])


def get_instructor_key(session: ApiSession, project_id: int) -> Result[str, str]:
    response = session.get(
        "/submission/instructor_key", params={"project_id": project_id}
    )

    result = api_utils.check_response(response)
    return result.map(lambda d: d["public_key"])


def get_submission_hash(
    session: ApiSession, submission_id: int
) -> Result[dto.SubmissionHashResponse, str]:
    response = session.get(f"/submission/{submission_id}/hash")

    result = api_utils.check_response(response)
    return result.map(lambda d: dto.SubmissionHashResponse(**d))


def download_submission_content(
    session: ApiSession, submission_id: int
) -> Result[bytes, str]:
    response = session.get(f"/submission/{submission_id}/content")

    return api_utils.check_response(response, raw_data=True)


def get_upload_key(session: ApiSession) -> Result[dto.UploadKeyResponse, str]:
    try:
        response = session.get("/pdf-to-audio/upload-key")
        result = api_utils.check_response(response)
        return result.map(lambda data: dto.UploadKeyResponse(**data))
    except Exception as e:
        return Result.Err(f"Network error: {e}")


def execute_pdf_to_audio(
    session: ApiSession, req: dto.PdfToAudioRequest
) -> Result[dto.PdfToAudioResponse, str]:
    try:
        response = session.post("/pdf-to-audio/execute", json=req.model_dump())
        result = api_utils.check_response(response)
        return result.map(lambda data: dto.PdfToAudioResponse(**data))
    except Exception as e:
        return Result.Err(f"Network error: {e}")
