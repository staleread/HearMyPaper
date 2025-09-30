import requests
from result import Result, Ok, Err

from .api import (
    create_project,
    update_project,
    get_project,
    get_projects,
)
from .dto import (
    ProjectCreateDto,
    ProjectUpdateDto,
    ProjectCreateResponse,
    ProjectResponse,
    ProjectListResponse,
    ProjectView,
)


def create_project_with_dto(
    session: requests.Session, project_dto: ProjectCreateDto
) -> Result[ProjectCreateResponse, str]:
    """
    Create a project using the form DTO.
    """
    try:
        create_request = project_dto.to_request()
        api_result = create_project(session, create_request)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error during project creation: {e}")


def update_project_with_dto(
    session: requests.Session, project_id: int, project_dto: ProjectUpdateDto
) -> Result[ProjectResponse, str]:
    """
    Update a project using the form DTO.
    """
    try:
        update_request = project_dto.to_request()
        api_result = update_project(session, project_id, update_request)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error during project update: {e}")


def get_project_as_view(
    session: requests.Session, project_id: int
) -> Result[ProjectView, str]:
    """
    Get a project and convert it to a view DTO.
    """
    try:
        api_result = get_project(session, project_id)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        project_response = api_result.unwrap()
        project_view = ProjectView.from_response(project_response)
        return Ok(project_view)
    except Exception as e:
        return Err(f"Unexpected error retrieving project: {e}")


def get_projects_list(
    session: requests.Session,
) -> Result[list[ProjectListResponse], str]:
    """
    Get list of projects.
    """
    try:
        api_result = get_projects(session)

        if api_result.is_err():
            return Err(api_result.unwrap_err())

        return Ok(api_result.unwrap())
    except Exception as e:
        return Err(f"Unexpected error retrieving projects: {e}")
