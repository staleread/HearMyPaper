from datetime import datetime, timedelta, timezone
from result import Ok
from ...shared.ui.catalog_screen import catalog_screen
from ..api import get_audit_logs


def audit_catalog_screen(navigator):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)

    result = get_audit_logs(navigator.session, start.isoformat(), end.isoformat())

    if result.is_ok():
        # Список списків для UI
        logs = [
            [
                str(log.timestamp),
                str(log.action),
                "✔" if log.is_success else "✖",
                str(log.reason or "-"),
                str(log.user_name or "-"),
            ]
            for log in result.unwrap()
        ]

    else:
        logs = []

    return catalog_screen(
        title="Audit Logs",
        headings=["Timestamp", "Action", "Success", "Reason", "User"],
        data=Ok(logs),
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=None,
    )
