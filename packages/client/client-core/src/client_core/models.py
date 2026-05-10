from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import StrEnum


class AccessLevel(StrEnum):
    UNCLASSIFIED = "UNCLASSIFIED"
    CONTROLLED = "CONTROLLED"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


@dataclass(frozen=True)
class User:
    id: str
    name: str
    surname: str
    email: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime


@dataclass(frozen=True)
class Project:
    id: UUID
    title: str
    description: str
    deadline: datetime


@dataclass(frozen=True)
class LabAttempt:
    id: UUID
    student_id: str
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None
    feedback: str | None = None
