from enum import StrEnum
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


class ProcessingTaskType(StrEnum):
    PDF_TO_AUDIO = "pdf_to_audio"
    UKRAINIAN_TTS = "ukrainian_tts"


@dataclass(frozen=True, slots=True)
class AssignmentDTO:
    assignment_id: UUID
    worker_id: UUID
    worker_public_key: bytes
    expires_at: datetime
