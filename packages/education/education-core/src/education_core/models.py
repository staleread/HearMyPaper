from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Project:
    id: UUID
    title: str
    description: str
    instructor_id: str
    deadline: datetime
    created_at: datetime
