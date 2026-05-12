from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from ...models import ProcessingTaskType, Conversion


@dataclass(frozen=True)
class ConversionRequestInfo:
    conversion_id: UUID
    sealing_key: bytes
    upload_url: str


class ProcessingPort(Protocol):
    async def request_conversion(
        self, source_id: UUID, task_type: ProcessingTaskType
    ) -> ConversionRequestInfo: ...

    async def commit_conversion(self, conversion_id: UUID) -> None: ...

    async def get_my_conversions(self) -> list[Conversion]: ...

    async def get_conversion_download_url(self, conversion_id: UUID) -> str: ...
