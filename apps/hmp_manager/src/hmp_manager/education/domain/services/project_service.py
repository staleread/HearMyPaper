from uuid import UUID
from ..models import Project
from ..ports import ProjectRepository, ProjectStudentRepository, IdentityService
from ..exceptions import (
    ProjectNotFoundError,
    StudentNotFoundError,
    StudentAlreadyAssignedError,
    StudentNotAssignedError,
)


class ProjectService:
    def __init__(
        self,
        projects: ProjectRepository,
        project_students: ProjectStudentRepository,
        identity: IdentityService,
    ):
        self.projects = projects
        self.project_students = project_students
        self.identity = identity

    async def get_projects(self, user_id: str) -> list[Project]:
        return await self.projects.get_projects_by_user_id(user_id)

    async def get_project(self, project_id: UUID) -> Project:
        project = await self.projects.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {project_id} not found")
        return project

    async def get_project_students(self, project_id: UUID) -> list[str]:
        # Verify project exists
        await self.get_project(project_id)
        return await self.project_students.get_student_ids(project_id)

    async def add_student_to_project(self, project_id: UUID, student_id: str) -> None:
        # Verify project exists
        await self.get_project(project_id)

        # Verify student exists in identity
        if not await self.identity.verify_student_exists(student_id):
            raise StudentNotFoundError(f"Student with id {student_id} not found")

        # Check if already assigned
        if await self.project_students.is_student_assigned(project_id, student_id):
            raise StudentAlreadyAssignedError(
                f"Student {student_id} is already assigned to project {project_id}"
            )

        await self.project_students.add_student(project_id, student_id)

    async def remove_student_from_project(
        self, project_id: UUID, student_id: str
    ) -> None:
        # Verify project exists
        await self.get_project(project_id)

        # Check if assigned
        if not await self.project_students.is_student_assigned(project_id, student_id):
            raise StudentNotAssignedError(
                f"Student {student_id} is not assigned to project {project_id}"
            )

        await self.project_students.remove_student(project_id, student_id)
