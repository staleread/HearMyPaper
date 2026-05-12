from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TaskAssignment:
    task_id: UUID
    sealing_key: bytes


@dataclass(frozen=True, slots=True)
class AcquireWorkerQuery:
    task_type: str


class AcquireWorkerPort(Protocol):
    async def __call__(self, query: AcquireWorkerQuery) -> TaskAssignment: ...
