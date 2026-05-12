from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DispatchTaskCommand:
    task_id: UUID
    source_download_url: str
    result_upload_url: str
    sealing_key: bytes


class DispatchTaskPort(Protocol):
    async def __call__(self, cmd: DispatchTaskCommand) -> None: ...
