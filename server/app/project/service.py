from app.shared.utils.db import SqlRunner

from . import repository as project_repo
from .models import Project
from .dto import (
    ProjectResponse,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectCreateResponse,
    StudentAssignmentRequest,
)


def get_project_by_id(id: int, *, db: SqlRunner) -> ProjectResponse:
    project, instructor_full_name = project_repo.get_project_with_instructor_username(
        id, db=db
    )
    instructor_email = project_repo.get_user_email_by_id(project.instructor_id, db=db)
    student_count = project_repo.get_project_student_count(id, db=db)

    return ProjectResponse(
        id=project.id,
        title=project.title,
        syllabus_summary=project.syllabus_summary,
        description=project.description,
        instructor_id=project.instructor_id,
        instructor_full_name=instructor_full_name,
        instructor_email=instructor_email,
        student_count=student_count,
        deadline=project.deadline,
    )


def create_project(
    req: ProjectCreateRequest, *, db: SqlRunner
) -> ProjectCreateResponse:
    # Resolve instructor email to ID
    instructor_id = project_repo.get_user_id_by_email(req.instructor_email, db=db)

    project = Project(
        title=req.title,
        syllabus_summary=req.syllabus_summary,
        description=req.description,
        instructor_id=instructor_id,
        deadline=req.deadline,
    )

    id = project_repo.create_project(project, db=db)

    return ProjectCreateResponse(id=id)


def update_project(
    id: int, req: ProjectUpdateRequest, *, db: SqlRunner
) -> ProjectResponse:
    # Resolve instructor email to ID
    instructor_id = project_repo.get_user_id_by_email(req.instructor_email, db=db)

    # Create updated project with all fields from request
    updated_project = Project(
        id=id,
        title=req.title,
        syllabus_summary=req.syllabus_summary,
        description=req.description,
        instructor_id=instructor_id,
        deadline=req.deadline,
    )

    project_repo.update_project(id, updated_project, db=db)

    # Return response with instructor username and student count
    return get_project_by_id(id, db=db)


def assign_students_to_project(
    project_id: int, req: StudentAssignmentRequest, *, db: SqlRunner
) -> ProjectResponse:
    # Assign students (this also verifies project exists)
    project_repo.assign_students_to_project(project_id, req.student_ids, db=db)

    # Return updated project
    return get_project_by_id(project_id, db=db)
