from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class HeartbeatCommand:
    worker_id: UUID


class HeartbeatPort(Protocol):
    async def __call__(self, cmd: HeartbeatCommand) -> None: ...
