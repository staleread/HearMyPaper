from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class WorkerNode:
    worker_id: UUID
    public_key: bytes  # The transient RSA/ECC key
    last_heartbeat: datetime
    load_score: int  # Current active tasks
    capabilities: list[str] = field(default_factory=list)
