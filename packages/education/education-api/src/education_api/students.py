from uuid import UUID
from typing import override

from blacksheep import FromJSON
from blacksheep.server.controllers import Controller, get, post, delete
from blacksheep.server.responses import ok, created, no_content, not_found, status_code
from blacksheep.server.authorization import auth
from pydantic import BaseModel

from education_core.exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    StudentAlreadyAssignedError,
    StudentNotAssignedError,
)
from education_core.ports.incoming import (
    GetProjectStudentsPort,
    AssignStudentToProjectPort,
    AssignStudentToProjectCommand,
    RemoveStudentFromProjectPort,
    RemoveStudentFromProjectCommand,
)


class StudentAssignmentRequest(BaseModel):
    student_id: str


class ProjectStudentsResponse(BaseModel):
    student_ids: list[str]


class Students(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/projects"

    def __init__(
        self,
        get_project_students: GetProjectStudentsPort,
        assign_student_to_project: AssignStudentToProjectPort,
        remove_student_from_project: RemoveStudentFromProjectPort,
    ) -> None:
        self.get_project_students = get_project_students
        self.assign_student_to_project = assign_student_to_project
        self.remove_student_from_project = remove_student_from_project

    @auth()
    @get("/{project_id}/students")
    async def get_project_students(self, project_id: UUID):
        try:
            student_ids = await self.get_project_students(project_id)
            return ok(ProjectStudentsResponse(student_ids=student_ids))
        except ProjectNotFoundError as e:
            return not_found(str(e))

    @auth()
    @post("/{project_id}/students")
    async def add_student_to_project(
        self, project_id: UUID, data: FromJSON[StudentAssignmentRequest]
    ):
        req = data.value
        cmd = AssignStudentToProjectCommand(
            project_id=project_id, student_id=req.student_id
        )
        try:
            await self.assign_student_to_project(cmd)
            return created()
        except (ProjectNotFoundError, StudentNotFoundError) as e:
            return not_found(str(e))
        except StudentAlreadyAssignedError as e:
            return status_code(409, str(e))

    @auth()
    @delete("/{project_id}/students/{student_id}")
    async def remove_student_from_project(self, project_id: UUID, student_id: str):
        cmd = RemoveStudentFromProjectCommand(
            project_id=project_id, student_id=student_id
        )
        try:
            await self.remove_student_from_project(cmd)
            return no_content()
        except (ProjectNotFoundError, StudentNotAssignedError) as e:
            return not_found(str(e))
