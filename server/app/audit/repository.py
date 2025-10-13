from app.shared.utils.db import SqlRunner

from app.shared.config.db import DataSource


def insert_action_log(
    action: str, is_success: bool, reason: str | None, *, db: SqlRunner
) -> None:
    # Use a new transaction so it's not rolled back when the request has failed
    db.transaction(DataSource.POSTGRES).query("""
        INSERT INTO action_logs (action, is_success, reason)
        VALUES (:action, :is_success, :reason)
    """).bind(action=action, is_success=is_success, reason=reason).execute()


def get_logs_between_timestamps(
    start_timestamp: str, end_timestamp: str, *, db: SqlRunner
) -> list[dict]:
    rows = (
        db.query("""
        SELECT timestamp, action, is_success, reason
        FROM action_logs
        WHERE timestamp >= :start_timestamp AND timestamp <= :end_timestamp
        ORDER BY timestamp DESC
    """)
        .bind(start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        .many_rows()
    )
    return rows
