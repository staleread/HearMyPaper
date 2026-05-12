from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from ...models import ProcessingTaskType


@dataclass(frozen=True)
class ConversionRequestInfo:
    conversion_id: UUID
    worker_public_key: bytes
    upload_url: str


class ProcessingPort(Protocol):
    async def request_conversion(
        self, lab_attempt_id: UUID, task_type: ProcessingTaskType
    ) -> ConversionRequestInfo: ...

    async def commit_conversion(self, conversion_id: UUID) -> None: ...
