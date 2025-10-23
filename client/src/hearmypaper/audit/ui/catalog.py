from textwrap import wrap

from datetime import datetime, timedelta, timezone
from ...shared.ui.catalog_screen import catalog_screen
from ..api import get_audit_logs


def audit_catalog_screen(navigator, date: datetime | None = None):
    if date is None:
        date = datetime.now(timezone.utc)

    # Ensure date is in UTC
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)

    data = (
        get_audit_logs(navigator.session, start.isoformat(), end.isoformat())
        .map(
            lambda logs: [
                [
                    str(log.timestamp),
                    str(log.action),
                    "✔" if log.is_success else "✖",
                    "\n".join(wrap(str(log.reason or "-"), width=50)),
                    str(log.user_name or "-"),
                    str(log.ip_address or "-"),
                ]
                for log in logs
            ]
        )
        .map_err(lambda err: f"Error loading audit logs: {err}")
    )

    logs_data = data.unwrap() if data.is_ok() else []

    def on_export(widget):
        navigator.navigate("audit_export_form", logs_data=logs_data, date=date)

    def on_prev_day(widget):
        prev_date = date - timedelta(days=1)
        navigator.navigate("audit_catalog", date=prev_date)

    def on_next_day(widget):
        next_date = date + timedelta(days=1)
        navigator.navigate("audit_catalog", date=next_date)

    actions = [
        ("Prev Day", on_prev_day),
        ("Next Day", on_next_day),
        ("Export", on_export),
    ]

    date_str = date.strftime("%Y-%m-%d")
    title = f"Audit Logs - {date_str}"

    return catalog_screen(
        title=title,
        headings=["Timestamp", "Action", "Success", "Reason", "User", "IP Address"],
        data=data,
        on_back=lambda w: navigator.navigate("resource_catalog"),
        actions=actions,
    )
