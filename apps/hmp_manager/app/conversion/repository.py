from uuid import UUID
from typing import Any
from hmp_core.storage import SqlRunner


def insert_conversion_job(
    submission_id: int, instructor_id: int, input_path: str, *, db: SqlRunner
) -> UUID:
    return (
        db.query("""
        INSERT INTO conversions (submission_id, instructor_id, input_path, status)
        VALUES (:submission_id, :instructor_id, :input_path, 'queued')
        RETURNING uuid
    """)
        .bind(
            submission_id=submission_id,
            instructor_id=instructor_id,
            input_path=input_path,
        )
        .scalar(lambda x: x)
    )


def get_conversion_by_uuid(
    conversion_uuid: UUID, *, db: SqlRunner
) -> dict[str, Any] | None:
    return (
        db.query("""
        SELECT c.*, u.pseudonym as instructor_pseudonym
        FROM conversions c
        JOIN users u ON c.instructor_id = u.id
        WHERE c.uuid = :uuid
    """)
        .bind(uuid=conversion_uuid)
        .first_row()
    )


def update_conversion_status(
    conversion_uuid: UUID,
    status: str,
    *,
    db: SqlRunner,
    error_message: str | None = None,
    output_path: str | None = None,
) -> None:
    db.query("""
        UPDATE conversions 
        SET status = :status, 
            error_message = :error_message,
            output_path = :output_path,
            updated_at = NOW()
        WHERE uuid = :uuid
    """).bind(
        status=status,
        uuid=conversion_uuid,
        error_message=error_message,
        output_path=output_path,
    ).execute()
