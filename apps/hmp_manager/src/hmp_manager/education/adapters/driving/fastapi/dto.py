from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str
    instructor_id: str
    deadline: datetime
    created_at: datetime


class StudentAssignmentRequest(BaseModel):
    student_id: str


class ProjectStudentsResponse(BaseModel):
    student_ids: list[str]
