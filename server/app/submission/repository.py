from app.shared.utils.db import SqlRunner


def insert_submission(
    project_student_id: int,
    title: str,
    encrypted_content: bytes,
    content_hash: str,
    *,
    db: SqlRunner,
) -> int:
    row = (
        db.query("""
        INSERT INTO submissions (project_student_id, title, content, content_hash)
        VALUES (:ps_id, :title, :content, :content_hash)
        RETURNING id
    """)
        .bind(
            ps_id=project_student_id,
            title=title,
            content=encrypted_content,
            content_hash=content_hash,
        )
        .one_row()
    )
    return row["id"]


def delete_submission(submission_id: int, *, db: SqlRunner) -> None:
    db.query("DELETE FROM submissions WHERE id = :id").bind(id=submission_id).execute()


def get_submissions_for_ui(*, db: SqlRunner) -> list[dict]:
    rows = db.query("""
        SELECT 
            s.id,
            s.title,
            CONCAT(st.name, ' ', st.surname) AS student_name,
            CONCAT(ins.name, ' ', ins.surname) AS instructor_name,
            s.submitted_at,
            s.content_hash
        FROM submissions s
        JOIN project_students ps ON ps.id = s.project_student_id
        JOIN users st ON st.id = ps.student_id
        JOIN projects p ON p.id = ps.project_id
        JOIN users ins ON ins.id = p.instructor_id
        ORDER BY s.submitted_at DESC
    """).many_rows()

    # Convert datetime to ISO string
    for row in rows:
        row["submitted_at"] = row["submitted_at"].isoformat()

    return rows


def get_submission_content_hash(submission_id: int, *, db: SqlRunner) -> str:
    row = (
        db.query("SELECT content_hash FROM submissions WHERE id = :id")
        .bind(id=submission_id)
        .one_row()
    )
    return row["content_hash"]


def get_submission_content(submission_id: int, *, db: SqlRunner) -> bytes:
    row = (
        db.query("SELECT content FROM submissions WHERE id = :id")
        .bind(id=submission_id)
        .one_row()
    )
    return row["content"]


def get_instructor_public_key(project_id: int, *, db: SqlRunner) -> bytes:
    row = (
        db.query("""
        SELECT public_key
        FROM users u
        JOIN projects p ON p.instructor_id = u.id
        WHERE p.id = :project_id
    """)
        .bind(project_id=project_id)
        .one_row()
    )
    return row["public_key"]


def get_project_student(
    student_id: int, project_id: int, *, db: SqlRunner
) -> int | None:
    """Get project_student ID if exists, otherwise return None."""
    row = (
        db.query("""
        SELECT id FROM project_students
        WHERE student_id = :student_id AND project_id = :project_id
    """)
        .bind(student_id=student_id, project_id=project_id)
        .first_row()
    )

    return row["id"] if row else None
