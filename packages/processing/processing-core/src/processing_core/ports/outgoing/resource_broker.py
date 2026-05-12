from typing import Protocol
from uuid import UUID
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TaskAssignment:
    task_id: UUID
    sealing_key: bytes


class ResourceBrokerPort(Protocol):
    async def acquire_task(self, task_type: str) -> TaskAssignment: ...

    async def start_task(
        self,
        task_id: UUID,
        source_download_url: str,
        result_upload_url: str,
        sealing_key: bytes,
    ) -> None: ...
