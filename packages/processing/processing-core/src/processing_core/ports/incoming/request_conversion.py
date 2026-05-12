from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from processing_core.models import ProcessingTaskType


@dataclass(frozen=True, slots=True)
class RequestConversionQuery:
    lab_attempt_id: UUID
    instructor_id: str
    task_type: ProcessingTaskType


@dataclass(frozen=True, slots=True)
class ConversionResponseDTO:
    conversion_id: UUID
    worker_public_key: bytes
    upload_url: str


class RequestConversionPort(Protocol):
    async def __call__(
        self, query: RequestConversionQuery
    ) -> ConversionResponseDTO: ...
