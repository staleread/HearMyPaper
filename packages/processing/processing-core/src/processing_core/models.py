from enum import StrEnum
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


class ConversionStatus(StrEnum):
    PENDING = "pending"
    COMMITTED = "committed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingTaskType(StrEnum):
    PDF_TO_AUDIO = "pdf_to_audio"
    UKRAINIAN_TTS = "ukrainian_tts"


@dataclass(frozen=True, slots=True)
class WorkerAssignment:
    assignment_id: UUID
    worker_id: UUID
    worker_public_key: bytes
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class AssignmentDTO:
    assignment_id: UUID
    worker_id: UUID
    worker_public_key: bytes
    upload_url: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class Conversion:
    conversion_id: UUID
    lab_attempt_id: UUID
    instructor_id: str
    worker_id: UUID
    status: ConversionStatus
    created_at: datetime
    updated_at: datetime
