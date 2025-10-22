from datetime import datetime, timedelta, timezone
from ...shared.ui.catalog_screen import catalog_screen
from ..api import get_audit_logs


def audit_catalog_screen(navigator):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)

    data = (
        get_audit_logs(navigator.session, start.isoformat(), end.isoformat())
        .map(
            lambda logs: [
                [
                    str(log.timestamp),
                    str(log.action),
                    "✔" if log.is_success else "✖",
                    str(log.reason or "-"),
                    str(log.user_name or "-"),
                ]
                for log in logs
            ]
        )
        .map_err(lambda err: f"Error loading audit logs: {err}")
    )

    return catalog_screen(
        title="Audit Logs",
        headings=["Timestamp", "Action", "Success", "Reason", "User"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=None,
    )
