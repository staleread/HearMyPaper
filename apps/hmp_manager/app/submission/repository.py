from uuid import UUID
from typing import Any
from hmp_core.storage import SqlRunner

def get_user_id_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> int | None:
    return db.query("""
        SELECT id FROM users WHERE pseudonym = :pseudonym
    """).bind(pseudonym=pseudonym).scalar(lambda x: x)

def get_project_student_id(project_id: int, user_id: int, *, db: SqlRunner) -> int | None:
    return db.query("""
        SELECT id FROM project_students 
        WHERE project_id = :project_id AND student_id = :user_id
    """).bind(
        project_id=project_id, 
        user_id=user_id
    ).scalar(lambda x: x)

def insert_pending_submission(
    project_student_id: int, 
    storage_path: str, 
    content_hash: str, 
    *, 
    db: SqlRunner
) -> UUID:
    return db.query("""
        INSERT INTO submissions (project_student_id, storage_path, content_hash, status)
        VALUES (:ps_id, :path, :hash, 'pending')
        RETURNING p_uuid
    """).bind(
        ps_id=project_student_id,
        path=storage_path,
        hash=content_hash
    ).scalar(lambda x: x)

def get_submission_by_uuid(submission_uuid: UUID, *, db: SqlRunner) -> dict[str, Any] | None:
    return db.query("""
        SELECT s.*, u.pseudonym as user_pseudonym
        FROM submissions s
        JOIN project_students ps ON s.project_student_id = ps.id
        JOIN users u ON ps.student_id = u.id
        WHERE s.p_uuid = :uuid
    """).bind(uuid=submission_uuid).first_row()

def update_submission_status(
    submission_uuid: UUID, 
    status: str, 
    *, 
    db: SqlRunner,
    log_action: str | None = None,
    log_context: dict[str, Any] | None = None,
    user_id: int | None = None,
    spiffe_id: str | None = None,
    pseudonym: str | None = None
) -> None:
    # Update status
    db.query("""
        UPDATE submissions SET status = :status WHERE p_uuid = :uuid
    """).bind(status=status, uuid=submission_uuid).execute()

    # Log action if requested
    if log_action:
        import json
        db.query("""
            INSERT INTO action_logs (actor_spiffe_id, actor_pseudonym, user_id, action, is_success, context)
            VALUES (:spiffe_id, :pseudonym, :user_id, :action, true, :context)
        """).bind(
            spiffe_id=spiffe_id,
            pseudonym=pseudonym,
            user_id=user_id,
            action=log_action,
            context=json.dumps(log_context) if log_context else None
        ).execute()
