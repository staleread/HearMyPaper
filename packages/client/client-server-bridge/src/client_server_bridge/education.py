from httpx import AsyncClient
from datetime import datetime
from uuid import UUID

from client_core.models import Project, LabAttempt
from client_core.ports.outgoing.education import EducationPort


class EducationPortAdapter(EducationPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_my_projects(self) -> list[Project]:
        response = await self.client.get("/projects")
        if response.status_code == 404:
            return []
        response.raise_for_status()
        data = response.json()
        return [
            Project(
                id=UUID(p["id"]),
                title=p["title"],
                description=p.get("description", ""),
                instructor_id=p["instructor_id"],
                deadline=datetime.fromisoformat(p["deadline"]),
            )
            for p in data
        ]

    async def get_project(self, project_id: UUID) -> Project | None:
        response = await self.client.get(f"/projects/{project_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        p = response.json()
        return Project(
            id=UUID(p["id"]),
            title=p["title"],
            description=p["description"],
            instructor_id=p["instructor_id"],
            deadline=datetime.fromisoformat(p["deadline"]),
        )

    async def get_project_students(self, project_id: UUID) -> list[str]:
        response = await self.client.get(f"/projects/{project_id}/students")
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()["student_ids"]

    async def assign_student(self, project_id: UUID, student_id: str) -> None:
        payload = {"student_id": student_id}
        response = await self.client.post(
            f"/projects/{project_id}/students", json=payload
        )
        response.raise_for_status()

    async def remove_student(self, project_id: UUID, student_id: str) -> None:
        response = await self.client.delete(
            f"/projects/{project_id}/students/{student_id}"
        )
        response.raise_for_status()

    async def get_project_attempts(self, project_id: UUID) -> list[LabAttempt]:
        response = await self.client.get(
            "/attempts", params={"project_id": str(project_id)}
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        data = response.json()
        return [
            LabAttempt(
                id=UUID(a["attempt_id"]),
                student_id=a["student_id"],
                submitted_at=datetime.fromisoformat(a["submitted_at"]),
                is_on_time=a["is_on_time"],
                grade=a.get("grade"),
                feedback=a.get("instructor_feedback"),
            )
            for a in data
        ]

    async def get_attempt(self, attempt_id: UUID) -> LabAttempt | None:
        response = await self.client.get(f"/attempts/{attempt_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        a = response.json()
        return LabAttempt(
            id=UUID(a["attempt_id"]),
            student_id=a["student_id"],
            submitted_at=datetime.fromisoformat(a["submitted_at"]),
            is_on_time=a["is_on_time"],
            grade=a.get("grade"),
            feedback=a.get("instructor_feedback"),
        )

    async def get_attempt_download_url(self, attempt_id: UUID) -> str:
        response = await self.client.get(f"/attempts/{attempt_id}/download-url")
        response.raise_for_status()
        return response.json()["download_url"]

    async def grade_attempt(
        self, attempt_id: UUID, grade: int, feedback: str | None
    ) -> None:
        payload = {
            "grade": grade,
            "feedback": feedback,
        }
        response = await self.client.post(
            f"/attempts/{attempt_id}/grade",
            json=payload,
        )
        response.raise_for_status()

    async def create_project(
        self, title: str, description: str, instructor_id: str, deadline: datetime
    ) -> Project:
        payload = {
            "title": title,
            "description": description,
            "instructor_id": instructor_id,
            "deadline": deadline.isoformat(),
        }
        response = await self.client.post("/projects", json=payload)
        response.raise_for_status()
        p = response.json()
        return Project(
            id=UUID(p["id"]),
            title=p["title"],
            description=p["description"],
            instructor_id=p["instructor_id"],
            deadline=datetime.fromisoformat(p["deadline"]),
        )

    async def update_project(
        self,
        project_id: UUID,
        title: str,
        description: str,
        instructor_id: str,
        deadline: datetime,
    ) -> Project:
        payload = {
            "title": title,
            "description": description,
            "instructor_id": instructor_id,
            "deadline": deadline.isoformat(),
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
        )
