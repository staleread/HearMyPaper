from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterWorkerCommand:
    worker_id: UUID
    public_key: bytes
    capabilities: list[str]


class RegisterWorkerPort(Protocol):
    async def __call__(self, cmd: RegisterWorkerCommand) -> None: ...
