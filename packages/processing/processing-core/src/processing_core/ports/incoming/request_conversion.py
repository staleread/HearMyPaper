from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from processing_core.models import ProcessingTaskType


@dataclass(frozen=True, slots=True)
class RequestConversionQuery:
    source_id: UUID
    subject_id: str
    task_type: ProcessingTaskType


@dataclass(frozen=True, slots=True)
class ConversionResponseDTO:
    conversion_id: UUID
    sealing_key: bytes
    upload_url: str


class RequestConversionPort(Protocol):
    async def __call__(
        self, query: RequestConversionQuery
    ) -> ConversionResponseDTO: ...
