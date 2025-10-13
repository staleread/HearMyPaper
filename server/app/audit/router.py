from typing import Annotated
from fastapi import APIRouter, Query

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize

from .dto import ActionLogResponse
from .decorators import audit

router = APIRouter()


@router.get("/")
@audit()
@authorize(AccessLevel.CONFIDENTIAL)
async def read_audit_logs(
    start: Annotated[str, Query()],
    end: Annotated[str, Query()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
) -> list[ActionLogResponse]:
    rows = (
        db.query("""
        SELECT 
            al.timestamp,
            al.action,
            al.is_success,
            al.reason,
            CASE 
                WHEN u.id IS NOT NULL THEN CONCAT(u.name, ' ', u.surname)
                ELSE NULL
            END AS user_name
        FROM action_logs al
        LEFT JOIN users u ON al.user_id = u.id
        WHERE al.timestamp >= :start_timestamp AND al.timestamp <= :end_timestamp
        ORDER BY al.timestamp DESC
    """)
        .bind(start_timestamp=start, end_timestamp=end)
        .many_rows()
    )
    return [
        ActionLogResponse(
            timestamp=row["timestamp"].isoformat(),
            action=row["action"],
            is_success=row["is_success"],
            reason=row["reason"],
            user_name=row["user_name"],
        )
        for row in rows
    ]
