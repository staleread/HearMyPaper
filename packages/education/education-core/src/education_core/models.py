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


@dataclass(frozen=True, slots=True)
class ProjectListItem:
    id: UUID
    title: str
    deadline: datetime


@dataclass(frozen=True, slots=True)
class LabAttempt:
    attempt_id: UUID
    student_id: str
    project_id: UUID
    submission_id: UUID
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None
    instructor_feedback: str | None = None


@dataclass(frozen=True, slots=True)
class AttemptListItem:
    attempt_id: UUID
    student_id: str
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None
