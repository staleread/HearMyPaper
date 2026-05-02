import ipinfo
from result import Result
from ..shared.utils.session import ApiSession
from . import api


def get_audit_logs(
    session: ApiSession, start: str, end: str
) -> Result[list[dict], str]:
    """
    Fetch audit logs and enrich them with location information based on IP addresses.

    Returns a Result containing a list of dictionaries with log data extended with a "Location" field.
    """
    logs_result = api.get_audit_logs(session, start, end)

    if logs_result.is_err():
        return logs_result

    logs = logs_result.unwrap()
    ip_set = {log.ip_address for log in logs if log.ip_address}

    location_map: dict[str, str] = {}
    handler = ipinfo.getHandler()

    for ip in ip_set:
        try:
            details = handler.getDetails(ip)
            city = getattr(details, "city", None)
            country = getattr(details, "country", None)

            if city and country:
                location_map[ip] = f"{city}, {country}"
            elif country:
                location_map[ip] = country
            else:
                location_map[ip] = "Unknown"
        except Exception:
            location_map[ip] = "Unknown"

    enriched_logs = []
    for log in logs:
        log_dict = {
            "timestamp": log.timestamp,
            "action": log.action,
            "is_success": log.is_success,
            "reason": log.reason,
            "user_name": log.user_name,
            "ip_address": log.ip_address,
            "location": location_map.get(log.ip_address, "Unknown")
            if log.ip_address
            else "Unknown",
        }
        enriched_logs.append(log_dict)

    from result import Ok

    return Ok(enriched_logs)
