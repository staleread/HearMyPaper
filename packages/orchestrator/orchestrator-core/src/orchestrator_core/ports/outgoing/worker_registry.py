from typing import Protocol
from uuid import UUID
from orchestrator_core.models import WorkerNode


class WorkerRegistryPort(Protocol):
    async def save_worker(self, worker: WorkerNode) -> None: ...

    async def get_active_workers(
        self, required_capability: str
    ) -> list[WorkerNode]: ...

    async def increment_worker_load(self, worker_id: UUID) -> None: ...

    async def decrement_worker_load(self, worker_id: UUID) -> None: ...
