from typing import Protocol
from uuid import UUID


class EventPublisherPort(Protocol):
    async def publish_task_dispatched(
        self,
        worker_id: UUID,
        task_id: UUID,
        task_type: str,
        source_download_url: str,
        result_upload_url: str,
        sealing_key: bytes,
    ) -> None: ...
