from dataclasses import dataclass
from typing import Protocol
from orchestrator_core.models import WorkerNode


@dataclass(frozen=True, slots=True)
class AcquireWorkerQuery:
    required_capability: str


class AcquireWorkerPort(Protocol):
    async def __call__(self, query: AcquireWorkerQuery) -> WorkerNode: ...
