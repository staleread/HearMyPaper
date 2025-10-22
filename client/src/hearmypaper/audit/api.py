from result import Ok, Err
from .dto import ActionLogResponse
from ..shared.utils.session import ApiSession


def get_audit_logs(session: ApiSession, start: str, end: str):
    try:
        response = session.get("/audit", params={"start": start, "end": end})
        if response.status_code == 200:
            logs_json = response.json()
            logs = [ActionLogResponse(**log) for log in logs_json]
            return Ok(logs)
        else:
            return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))
