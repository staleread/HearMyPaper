from typing import Annotated
from fastapi import APIRouter, Query

from app.shared.dependencies.db import PostgresRunnerDep
from app.auth.dependencies import CurrentSubjectDep
from app.auth.enums import AccessLevel
from app.auth.decorators import authorize

from . import repository as audit_repo
from .models import ActionLog
from .decorators import audit

router = APIRouter()


@router.get("/")
@authorize(AccessLevel.CONFIDENTIAL)
@audit()
async def read_audit_logs(
    start: Annotated[str, Query()],
    end: Annotated[str, Query()],
    db: PostgresRunnerDep,
    subject: CurrentSubjectDep,
) -> list[ActionLog]:
    rows = audit_repo.get_logs_between_timestamps(start, end, db=db)
    return [
        ActionLog(
            timestamp=row["timestamp"].isoformat(),
            action=row["action"],
            is_success=row["is_success"],
            reason=row["reason"],
        )
        for row in rows
    ]
