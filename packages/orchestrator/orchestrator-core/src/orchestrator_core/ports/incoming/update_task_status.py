from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from orchestrator_core.models import TaskStatus


@dataclass(frozen=True, slots=True)
class UpdateTaskStatusCommand:
    task_id: UUID
    status: TaskStatus


class UpdateTaskStatusPort(Protocol):
    async def __call__(self, cmd: UpdateTaskStatusCommand) -> None: ...
