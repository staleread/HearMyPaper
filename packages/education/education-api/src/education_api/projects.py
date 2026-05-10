from datetime import datetime
from uuid import UUID
from typing import override

from blacksheep import FromJSON, Request
from blacksheep.server.controllers import Controller, get, post, put
from blacksheep.server.responses import ok, created, not_found, status_code
from blacksheep.server.authorization import auth
from pydantic import BaseModel

from education_core.exceptions import (
    ProjectNotFoundError,
    ProjectAlreadyExistsError,
)
from education_core.ports.incoming import (
    GetProjectPort,
    GetUserProjectsPort,
    CreateProjectPort,
    CreateProjectCommand,
    UpdateProjectPort,
    UpdateProjectCommand,
)


class ProjectCreateRequest(BaseModel):
    title: str
    description: str
    deadline: datetime


class ProjectUpdateRequest(BaseModel):
    title: str
    description: str
    deadline: datetime


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str
    instructor_id: str
    deadline: datetime
    created_at: datetime


class ProjectsController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/projects"

    def __init__(
        self,
        get_user_projects_port: GetUserProjectsPort,
        get_project_port: GetProjectPort,
        create_project_port: CreateProjectPort,
        update_project_port: UpdateProjectPort,
    ) -> None:
        self.get_user_projects_port = get_user_projects_port
        self.get_project_port = get_project_port
        self.create_project_port = create_project_port
        self.update_project_port = update_project_port

    @auth()
    @get("/")
    async def get_projects(self, request: Request):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not found in token")

        projects = await self.get_user_projects_port(user_id)
        return ok(
            [
                ProjectResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    instructor_id=p.instructor_id,
                    deadline=p.deadline,
                    created_at=p.created_at,
                )
                for p in projects
            ]
        )

    @auth()
    @get("/{project_id}")
    async def get_project(self, project_id: UUID):
        try:
            p = await self.get_project_port(project_id)
            return ok(
                ProjectResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    instructor_id=p.instructor_id,
                    deadline=p.deadline,
                    created_at=p.created_at,
                )
            )
        except ProjectNotFoundError as e:
            return not_found(str(e))

    @auth()
    @post("/")
    async def create_project(
        self, request: Request, data: FromJSON[ProjectCreateRequest]
    ):
        user_id = request.user.claims.get("sub")
        if not user_id:
            return status_code(401, "User ID not found in token")

        req = data.value
        cmd = CreateProjectCommand(
            title=req.title,
            description=req.description,
            instructor_id=user_id,
            deadline=req.deadline,
        )
        try:
            p = await self.create_project_port(cmd)
            return created(
                ProjectResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    instructor_id=p.instructor_id,
                    deadline=p.deadline,
                    created_at=p.created_at,
                ),
                f"/projects/{p.id}",
            )
        except ProjectAlreadyExistsError as e:
            return status_code(409, str(e))

    @auth()
    @put("/{project_id}")
    async def update_project(
        self, project_id: UUID, data: FromJSON[ProjectUpdateRequest]
    ):
        req = data.value
        cmd = UpdateProjectCommand(
            title=req.title,
            description=req.description,
            deadline=req.deadline,
        )
        try:
            p = await self.update_project_port(project_id, cmd)
            return ok(
                ProjectResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    instructor_id=p.instructor_id,
                    deadline=p.deadline,
                    created_at=p.created_at,
                )
            )
        except ProjectNotFoundError as e:
            return not_found(str(e))
        except ProjectAlreadyExistsError as e:
            return status_code(409, str(e))
