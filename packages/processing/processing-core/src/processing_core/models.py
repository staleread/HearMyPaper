from enum import StrEnum
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


class ConversionStatus(StrEnum):
    PENDING = "pending"
    COMMITTED = "committed"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"


class ProcessingTaskType(StrEnum):
    PDF_TO_AUDIO = "pdf_to_audio"


@dataclass(frozen=True, slots=True)
class Conversion:
    conversion_id: UUID
    source_id: UUID
    subject_id: str
    task_id: UUID
    status: ConversionStatus
    created_at: datetime
    updated_at: datetime
