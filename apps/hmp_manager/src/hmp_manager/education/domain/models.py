from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Project(BaseModel):
    id: UUID
    title: str
    description: str
    instructor_id: str
    deadline: datetime
    created_at: datetime
