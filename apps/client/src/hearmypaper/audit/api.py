from result import Err
from pydantic import TypeAdapter
from .dto import ActionLogResponse
from ..shared.utils.session import ApiSession
from ..shared.utils.api import check_response


def get_audit_logs(session: ApiSession, start: str, end: str):
    try:
        r = session.get("/audit/", params={"start": start, "end": end})
        result = check_response(r)
        return result.map(
            lambda data: TypeAdapter(list[ActionLogResponse]).validate_python(data)
        )
    except Exception as e:
        return Err(f"Network error: {e}")
