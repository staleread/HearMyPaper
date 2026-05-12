from enum import StrEnum
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


class ConversionStatus(StrEnum):
    PENDING = "pending"
    COMMITTED = "committed"


class ProcessingTaskType(StrEnum):
    PDF_TO_AUDIO = "pdf_to_audio"


@dataclass(frozen=True, slots=True)
class Conversion:
    conversion_id: UUID
    lab_attempt_id: UUID
    instructor_id: str
    task_id: UUID
    status: ConversionStatus
    created_at: datetime
    updated_at: datetime
