from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


class TaskStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class WorkerNode:
    worker_id: UUID
    public_key: bytes
    load_score: int  # Current active tasks
    capabilities: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ConversionTask:
    task_id: UUID
    worker_id: UUID
    task_type: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
