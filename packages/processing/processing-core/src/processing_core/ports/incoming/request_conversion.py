from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from processing_core.models import AssignmentDTO, ProcessingTaskType


@dataclass(frozen=True, slots=True)
class RequestConversionQuery:
    lab_attempt_id: UUID
    instructor_id: str  # VARCHAR(75)
    task_type: ProcessingTaskType


class RequestConversionPort(Protocol):
    async def __call__(self, query: RequestConversionQuery) -> AssignmentDTO: ...
