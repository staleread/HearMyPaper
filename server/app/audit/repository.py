from app.shared.utils.db import SqlRunner

from app.shared.config.db import DataSource


def insert_action_log(
    action: str,
    is_success: bool,
    reason: str | None,
    user_id: int | None,
    ip_address: str | None,
    *,
    db: SqlRunner,
) -> None:
    # Use a new transaction so it's not rolled back when the request has failed
    db.transaction(DataSource.POSTGRES).query("""
        INSERT INTO action_logs (action, is_success, reason, user_id, ip_address)
        VALUES (:action, :is_success, :reason, :user_id, :ip_address)
    """).bind(
        action=action,
        is_success=is_success,
        reason=reason,
        user_id=user_id,
        ip_address=ip_address,
    ).execute()
