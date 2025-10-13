from app.shared.utils.db import SqlRunner
from . import repository as audit_repo


def add_action_log(
    action: str,
    is_success: bool,
    reason: str | None,
    user_id: int | None,
    *,
    db: SqlRunner,
) -> None:
    audit_repo.insert_action_log(
        action=action,
        is_success=is_success,
        reason=reason,
        user_id=user_id,
        db=db,
    )
