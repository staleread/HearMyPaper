from orchestrator_core.models import TaskStatus
from orchestrator_core.ports.incoming.update_task_status import (
    UpdateTaskStatusPort,
    UpdateTaskStatusCommand,
)
from orchestrator_core.ports.outgoing.task_repository import TaskRepositoryPort
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort
from orchestrator_core.exceptions import TaskNotFoundError


class UpdateTaskStatusUseCase(UpdateTaskStatusPort):
    def __init__(self, tasks: TaskRepositoryPort, registry: WorkerRegistryPort):
        self._tasks = tasks
        self._registry = registry

    async def __call__(self, cmd: UpdateTaskStatusCommand) -> None:
        task = await self._tasks.get_task(cmd.task_id)
        if not task:
            raise TaskNotFoundError(f"Task {cmd.task_id} not found")

        await self._tasks.update_task_status(cmd.task_id, cmd.status.value)

        # If terminal status, decrement worker load
        if cmd.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            await self._registry.decrement_worker_load(task.worker_id)

            # TODO: Notify processing module about completion/failure
            # This could be via another outgoing event
