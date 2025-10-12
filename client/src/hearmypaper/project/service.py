import requests
from result import Result

from . import api
from .dto import (
    ProjectCreateDto,
    ProjectUpdateDto,
    ProjectResponse,
    ProjectCreateResponse,
    ProjectListResponse,
    ProjectView,
    StudentAssignmentDto,
)


def create_project(
    session: requests.Session, project_dto: ProjectCreateDto
) -> Result[ProjectCreateResponse, str]:
    create_request = project_dto.to_request()
    return api.create_project(session, create_request)


def update_project(
    session: requests.Session, project_id: int, project_dto: ProjectUpdateDto
) -> Result[ProjectResponse, str]:
    update_request = project_dto.to_request()
    return api.update_project(session, project_id, update_request)


def get_project(session: requests.Session, project_id: int) -> Result[ProjectView, str]:
    return api.get_project(session, project_id).map(ProjectView.from_response)


def get_projects(session: requests.Session) -> Result[list[ProjectListResponse], str]:
    return api.get_projects(session)


def assign_students(
    session: requests.Session, project_id: int, assignment_dto: StudentAssignmentDto
) -> Result[ProjectResponse, str]:
    assignment_request = assignment_dto.to_request()
    return api.assign_students(session, project_id, assignment_request)
