from app.shared.utils.db import SqlRunner
from . import repository


def create_submission(
    project_student_id: int, title: str, encrypted_content: bytes, *, db: SqlRunner
) -> int:
    return repository.insert_submission(
        project_student_id, title, encrypted_content, db=db
    )


def remove_submission(submission_id: int, *, db: SqlRunner) -> None:
    repository.delete_submission(submission_id, db=db)


def list_submissions_for_ui(*, db: SqlRunner) -> list[dict]:
    return repository.get_submissions_for_ui(db=db)


def get_instructor_key(project_id: int, *, db: SqlRunner) -> str:
    return repository.get_instructor_public_key(project_id, db=db)


def create_project_for_student(
    student_id: int, instructor_id: int, *, db: SqlRunner
) -> int:
    project_row = (
        db.query("""
        INSERT INTO projects (instructor_id)
        VALUES (:instructor_id)
        RETURNING id
    """)
        .bind(instructor_id=instructor_id)
        .one_row()
    )
    project_id = project_row["id"]

    ps_row = (
        db.query("""
        INSERT INTO projects_students (student_id, project_id)
        VALUES (:student_id, :project_id)
        RETURNING id
    """)
        .bind(student_id=student_id, project_id=project_id)
        .one_row()
    )

    return ps_row["id"]
