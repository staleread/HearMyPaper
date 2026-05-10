from httpx import AsyncClient
from datetime import datetime
from uuid import UUID
from typing import override

from education_core.models import Project, ProjectListItem, AttemptListItem
from education_core.ports.incoming import (
    GetUserProjectsPort,
    GetProjectPort,
    CreateProjectPort,
    UpdateProjectPort,
    GetProjectAttemptsPort,
    ViewSubmissionPort,
    GradeLabAttemptPort,
    GetProjectStudentsPort,
    AssignStudentToProjectPort,
    RemoveStudentFromProjectPort,
    CreateProjectCommand,
    UpdateProjectCommand,
    GradeLabAttemptCommand,
    AssignStudentToProjectCommand,
    RemoveStudentFromProjectCommand,
)


class GetUserProjectsAdapter(GetUserProjectsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, user_id: str) -> list[ProjectListItem]:
        response = await self.client.get("/projects/")
        response.raise_for_status()
        data = response.json()
        return [
            ProjectListItem(
                id=UUID(p["id"]),
                title=p["title"],
                deadline=datetime.fromisoformat(p["deadline"]),
            )
            for p in data
        ]


class GetProjectAdapter(GetProjectPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, project_id: UUID) -> Project:
        response = await self.client.get(f"/projects/{project_id}")
        response.raise_for_status()
        p = response.json()
        return Project(
            id=UUID(p["id"]),
            title=p["title"],
            description=p["description"],
            instructor_id=p["instructor_id"],
            deadline=datetime.fromisoformat(p["deadline"]),
            created_at=datetime.fromisoformat(p["created_at"]),
        )


class CreateProjectAdapter(CreateProjectPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: CreateProjectCommand) -> Project:
        payload = {
            "title": cmd.title,
            "description": cmd.description,
            "deadline": cmd.deadline.isoformat(),
        }
        response = await self.client.post("/projects/", json=payload)
        response.raise_for_status()
        p = response.json()
        return Project(
            id=UUID(p["id"]),
            title=p["title"],
            description=p["description"],
            instructor_id=p["instructor_id"],
            deadline=datetime.fromisoformat(p["deadline"]),
            created_at=datetime.fromisoformat(p["created_at"]),
        )


class UpdateProjectAdapter(UpdateProjectPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, project_id: UUID, cmd: UpdateProjectCommand) -> Project:
        payload = {
            "title": cmd.title,
            "description": cmd.description,
            "deadline": cmd.deadline.isoformat(),
        }
        response = await self.client.put(f"/projects/{project_id}", json=payload)
        response.raise_for_status()
        p = response.json()
        return Project(
            id=UUID(p["id"]),
            title=p["title"],
            description=p["description"],
            instructor_id=p["instructor_id"],
            deadline=datetime.fromisoformat(p["deadline"]),
            created_at=datetime.fromisoformat(p["created_at"]),
        )


class GetProjectAttemptsAdapter(GetProjectAttemptsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, project_id: UUID) -> list[AttemptListItem]:
        response = await self.client.get(f"/projects/{project_id}/attempts/")
        response.raise_for_status()
        data = response.json()
        return [
            AttemptListItem(
                attempt_id=UUID(a["attempt_id"]),
                student_id=a["student_id"],
                submitted_at=datetime.fromisoformat(a["submitted_at"]),
                is_on_time=a["is_on_time"],
                grade=a.get("grade"),
            )
            for a in data
        ]


class ViewSubmissionAdapter(ViewSubmissionPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, instructor_id: str, submission_id: UUID) -> str:
        response = await self.client.get(f"/attempts/{submission_id}/download-url")
        response.raise_for_status()
        return response.json()["download_url"]


class GradeLabAttemptAdapter(GradeLabAttemptPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: GradeLabAttemptCommand) -> None:
        payload = {
            "grade": cmd.grade,
            "feedback": cmd.feedback,
        }
        response = await self.client.post(
            f"/attempts/{cmd.attempt_id}/grade",
            json=payload,
        )
        response.raise_for_status()


class GetProjectStudentsAdapter(GetProjectStudentsPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, project_id: UUID) -> list[str]:
        response = await self.client.get(f"/projects/{project_id}/students")
        response.raise_for_status()
        return response.json()["student_ids"]


class AssignStudentToProjectAdapter(AssignStudentToProjectPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: AssignStudentToProjectCommand) -> None:
        payload = {"student_id": cmd.student_id}
        response = await self.client.post(
            f"/projects/{cmd.project_id}/students", json=payload
        )
        response.raise_for_status()


class RemoveStudentFromProjectAdapter(RemoveStudentFromProjectPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: RemoveStudentFromProjectCommand) -> None:
        response = await self.client.delete(
            f"/projects/{cmd.project_id}/students/{cmd.student_id}"
        )
        response.raise_for_status()
