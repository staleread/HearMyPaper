from fastapi.exceptions import HTTPException

from app.shared.utils.db import SqlRunner

from .models import Project


def get_project_by_id(id: int, *, db: SqlRunner) -> Project:
    row = (
        db.query("""
        SELECT id, title, syllabus_summary, description, instructor_id, deadline
        FROM projects
        WHERE id = :id
    """)
        .bind(id=id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404, detail=f"Project {id} not found")

    return Project(
        id=row["id"],
        title=row["title"],
        syllabus_summary=row["syllabus_summary"],
        description=row["description"],
        instructor_id=row["instructor_id"],
        deadline=row["deadline"],
    )


def get_project_with_instructor_username(
    id: int, *, db: SqlRunner
) -> tuple[Project, str]:
    row = (
        db.query("""
        SELECT p.id, p.title, p.syllabus_summary, p.description, p.instructor_id, p.deadline, CONCAT(u.name, ' ', u.surname) as username
        FROM projects p
        JOIN users u ON p.instructor_id = u.id
        WHERE p.id = :id
    """)
        .bind(id=id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404, detail=f"Project {id} not found")

    project = Project(
        id=row["id"],
        title=row["title"],
        syllabus_summary=row["syllabus_summary"],
        description=row["description"],
        instructor_id=row["instructor_id"],
        deadline=row["deadline"],
    )

    return project, row["username"]


def get_project_student_count(project_id: int, *, db: SqlRunner) -> int:
    return (
        db.query("""
        SELECT COUNT(*)
        FROM project_students
        WHERE project_id = :project_id
    """)
        .bind(project_id=project_id)
        .scalar(lambda x: int(x))
    )


def create_project(project: Project, *, db: SqlRunner) -> int:
    return (
        db.query("""
            INSERT INTO projects (title, syllabus_summary, description, instructor_id, deadline)
            VALUES (:title, :syllabus_summary, :description, :instructor_id, :deadline)
            RETURNING id
        """)
        .bind(
            title=project.title,
            syllabus_summary=project.syllabus_summary,
            description=project.description,
            instructor_id=project.instructor_id,
            deadline=project.deadline,
        )
        .scalar(lambda x: int(x))
    )


def update_project(id: int, project: Project, *, db: SqlRunner) -> None:
    # First verify the project exists
    get_project_by_id(id, db=db)

    # Execute the update
    db.query("""
        UPDATE projects
        SET title = :title, syllabus_summary = :syllabus_summary,
            description = :description, instructor_id = :instructor_id, deadline = :deadline
        WHERE id = :id
    """).bind(
        id=id,
        title=project.title,
        syllabus_summary=project.syllabus_summary,
        description=project.description,
        instructor_id=project.instructor_id,
        deadline=project.deadline,
    ).execute()


def assign_students_to_project(
    project_id: int, student_ids: list[int], *, db: SqlRunner
) -> None:
    # Verify project exists
    get_project_by_id(project_id, db=db)

    # Remove existing assignments
    db.query("""
        DELETE FROM project_students
        WHERE project_id = :project_id
    """).bind(project_id=project_id).execute()

    # Add new assignments
    if student_ids:
        for student_id in student_ids:
            db.query("""
                INSERT INTO project_students (project_id, student_id)
                VALUES (:project_id, :student_id)
            """).bind(project_id=project_id, student_id=student_id).execute()


def get_user_id_by_email(email: str, *, db: SqlRunner) -> int:
    """Get user ID by email address"""
    row = (
        db.query("""
        SELECT id
        FROM users
        WHERE email = :email
    """)
        .bind(email=email)
        .first_row()
    )

    if not row:
        raise HTTPException(
            status_code=400, detail=f"User with email {email} not found"
        )

    return row["id"]


def get_user_email_by_id(user_id: int, *, db: SqlRunner) -> str:
    """Get user email by ID"""
    row = (
        db.query("""
        SELECT email
        FROM users
        WHERE id = :user_id
    """)
        .bind(user_id=user_id)
        .first_row()
    )

    if not row:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    return row["email"]
