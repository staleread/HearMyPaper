from ..shared.utils.session import ApiSession
from result import Result, Err
from pydantic import parse_obj_as

from .dto import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectUpdateRequest,
    ProjectResponse,
    ProjectListResponse,
    StudentAssignmentRequest,
)
from ..shared.utils.api import check_response


def get_projects(session: ApiSession) -> Result[list[ProjectListResponse], str]:
    try:
        r = session.get("/project/")
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(list[ProjectListResponse], data))
    except Exception as e:
        return Err(f"Network error: {e}")


def get_project(session: ApiSession, project_id: int) -> Result[ProjectResponse, str]:
    try:
        r = session.get(f"/project/{project_id}")
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(ProjectResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def create_project(
    session: ApiSession, req: ProjectCreateRequest
) -> Result[ProjectCreateResponse, str]:
    try:
        r = session.post("/project/", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(ProjectCreateResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def update_project(
    session: ApiSession, project_id: int, req: ProjectUpdateRequest
) -> Result[ProjectResponse, str]:
    try:
        r = session.put(f"/project/{project_id}", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(ProjectResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def assign_students(
    session: ApiSession, project_id: int, req: StudentAssignmentRequest
) -> Result[ProjectResponse, str]:
    try:
        r = session.put(f"/project/{project_id}/students", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: parse_obj_as(ProjectResponse, data))
    except Exception as e:
        return Err(f"Network error: {e}")


def get_project_students(
    session: ApiSession, project_id: int
) -> Result[list[str], str]:
    """Get list of student emails assigned to a project."""
    try:
        r = session.get(f"/project/{project_id}/students")
        result = check_response(r)
        return result.map(
            lambda data: [student["email"] for student in data]  # type: ignore[index]
        )
    except Exception as e:
        return Err(f"Network error: {e}")
