from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import StrEnum


class AccessLevel(StrEnum):
    UNCLASSIFIED = "UNCLASSIFIED"
    CONTROLLED = "CONTROLLED"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


class ProcessingTaskType(StrEnum):
    PDF_TO_AUDIO = "pdf_to_audio"


class ConversionStatus(StrEnum):
    PENDING = "pending"
    COMMITTED = "committed"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Conversion:
    id: UUID
    source_id: UUID
    status: ConversionStatus
    created_at: datetime


@dataclass(frozen=True)
class FileInfo:
    path: str
    name: str
    extension: str


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
    instructor_id: str
    deadline: datetime


@dataclass(frozen=True)
class LabAttempt:
    id: UUID
    project_id: UUID
    student_id: str
    submitted_at: datetime
    is_on_time: bool
    grade: int | None = None
    feedback: str | None = None
