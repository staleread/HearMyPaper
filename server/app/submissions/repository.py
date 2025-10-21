from app.shared.utils.db import SqlRunner


def insert_submission(
    project_student_id: int, title: str, encrypted_content: bytes, *, db: SqlRunner
) -> int:
    row = (
        db.query("""
        INSERT INTO submissions (project_student_id, title, content)
        VALUES (:ps_id, :title, :content)
        RETURNING id
    """)
        .bind(ps_id=project_student_id, title=title, content=encrypted_content)
        .one_row()
    )
    return row["id"]


def delete_submission(submission_id: int, *, db: SqlRunner) -> None:
    db.query("DELETE FROM submissions WHERE id = :id").bind(id=submission_id).execute()


def get_submissions_for_ui(*, db: SqlRunner) -> list[dict]:
    return db.query("""
        SELECT 
            s.id,
            s.title,
            CONCAT(st.name, ' ', st.surname) AS student_name,
            CONCAT(ins.name, ' ', ins.surname) AS instructor_name,
            s.submitted_at
        FROM submissions s
        JOIN projects_students ps ON ps.id = s.project_student_id
        JOIN students st ON st.id = ps.student_id
        JOIN projects p ON p.id = ps.project_id
        JOIN instructors ins ON ins.id = p.instructor_id
        ORDER BY s.submitted_at DESC
    """).many_rows()


def get_instructor_public_key(project_id: int, *, db: SqlRunner) -> str:
    row = (
        db.query("""
        SELECT public_key
        FROM instructors ins
        JOIN projects p ON p.instructor_id = ins.id
        WHERE p.id = :project_id
    """)
        .bind(project_id=project_id)
        .one_row()
    )
    return row["public_key"]
