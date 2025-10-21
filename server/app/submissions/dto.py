from datetime import datetime
from pydantic import BaseModel


class SubmissionResponse(BaseModel):
    id: int
    title: str
    student_name: str
    instructor_name: str
    submitted_at: datetime


class SubmissionCreateRequest(BaseModel):
    project_student_id: int
    title: str
    encrypted_content: bytes
