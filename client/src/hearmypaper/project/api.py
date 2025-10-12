import requests
from result import Result, Err

from .dto import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectUpdateRequest,
    ProjectResponse,
    ProjectListResponse,
    StudentAssignmentRequest,
)
from ..shared.utils.api import check_response


# Project endpoints
def get_projects(session: requests.Session) -> Result[list[ProjectListResponse], str]:
    """Get list of projects"""
    try:
        r = session.get("https://localhost/project/")
        result = check_response(r)
        return result.map(lambda data: [ProjectListResponse(**item) for item in data])
    except Exception as e:
        return Err(f"Network error: {e}")


def get_project(
    session: requests.Session, project_id: int
) -> Result[ProjectResponse, str]:
    """Get full project details"""
    try:
        r = session.get(f"https://localhost/project/{project_id}")
        result = check_response(r)
        return result.map(lambda data: ProjectResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def create_project(
    session: requests.Session, req: ProjectCreateRequest
) -> Result[ProjectCreateResponse, str]:
    """Create a new project"""
    try:
        r = session.post("https://localhost/project/", json=req.model_dump())
        result = check_response(r)
        return result.map(lambda data: ProjectCreateResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def update_project(
    session: requests.Session, project_id: int, req: ProjectUpdateRequest
) -> Result[ProjectResponse, str]:
    """Update an existing project"""
    try:
        r = session.put(
            f"https://localhost/project/{project_id}", json=req.model_dump()
        )
        result = check_response(r)
        return result.map(lambda data: ProjectResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")


def assign_students(
    session: requests.Session, project_id: int, req: StudentAssignmentRequest
) -> Result[ProjectResponse, str]:
    """Assign students to a project by their emails"""
    try:
        r = session.put(
            f"https://localhost/project/{project_id}/students", json=req.model_dump()
        )
        result = check_response(r)
        return result.map(lambda data: ProjectResponse(**data))
    except Exception as e:
        return Err(f"Network error: {e}")
