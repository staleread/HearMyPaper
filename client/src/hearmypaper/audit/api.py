import requests
from result import Ok, Err
from .dto import ActionLogResponse

BASE_URL = "https://localhost"  # заміни на свій бекенд


def get_audit_logs(session: requests.Session, start: str, end: str):
    """
    Завантажує логи аудиту за проміжок часу.
    start, end: ISO-формат дати (UTC)
    Повертає Result[List[AuditLog], str]
    """
    try:
        response = session.get(f"{BASE_URL}/audit", params={"start": start, "end": end})
        if response.status_code == 200:
            logs_json = response.json()
            logs = [ActionLogResponse(**log) for log in logs_json]
            return Ok(logs)
        else:
            return Err(f"{response.status_code}: {response.text}")
    except Exception as e:
        return Err(str(e))
