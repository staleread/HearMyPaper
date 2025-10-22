import base64
import hashlib
from app.shared.utils.db import SqlRunner
from . import repository


class SubmissionError(Exception):
    """Custom exception for submission errors."""

    pass


def create_submission(
    project_id: int,
    student_id: int,
    title: str,
    encrypted_content: bytes,
    *,
    db: SqlRunner,
) -> int:
    content_hash = hashlib.md5(encrypted_content).hexdigest()
    project_student_id = repository.get_project_student(student_id, project_id, db=db)

    if project_student_id is None:
        raise SubmissionError("Student is not assigned to this project")

    return repository.insert_submission(
        project_student_id, title, encrypted_content, content_hash, db=db
    )


def remove_submission(submission_id: int, *, db: SqlRunner) -> None:
    repository.delete_submission(submission_id, db=db)


def list_submissions_for_ui(*, db: SqlRunner) -> list[dict]:
    return repository.get_submissions_for_ui(db=db)


def get_submission_hash(submission_id: int, *, db: SqlRunner) -> str:
    return repository.get_submission_content_hash(submission_id, db=db)


def get_submission_content(submission_id: int, *, db: SqlRunner) -> bytes:
    return repository.get_submission_content(submission_id, db=db)


def get_instructor_key(project_id: int, *, db: SqlRunner) -> str:
    key_bytes = repository.get_instructor_public_key(project_id, db=db)
    return base64.b64encode(key_bytes).decode("utf-8")
