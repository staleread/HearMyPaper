from pydantic import BaseModel


class Project(BaseModel):
    id: int = 0
    title: str
    syllabus_summary: str
    description: str
    instructor_id: int
    deadline: str  # ISO string format
