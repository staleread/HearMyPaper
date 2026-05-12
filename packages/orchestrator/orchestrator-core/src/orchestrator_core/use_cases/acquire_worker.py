from uuid import uuid4
from datetime import datetime, UTC
from orchestrator_core.models import ConversionTask, TaskStatus
from orchestrator_core.exceptions import NoWorkerAvailableError
from orchestrator_core.ports.incoming.acquire_worker import (
    AcquireWorkerPort,
    AcquireWorkerQuery,
    TaskAssignment,
)
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort
from orchestrator_core.ports.outgoing.task_repository import TaskRepositoryPort


class AcquireWorkerUseCase(AcquireWorkerPort):
    DDOS_THRESHOLD = 20

    def __init__(self, registry: WorkerRegistryPort, tasks: TaskRepositoryPort):
        self._registry = registry
        self._tasks = tasks

    async def __call__(self, query: AcquireWorkerQuery) -> TaskAssignment:
        active_workers = await self._registry.get_active_workers(query.task_type)

        if not active_workers:
            raise NoWorkerAvailableError(
                f"No active workers with capability '{query.task_type}'"
            )

        # Sort by load_score (lowest first)
        active_workers.sort(key=lambda w: w.load_score)

        best_worker = active_workers[0]

        if best_worker.load_score >= self.DDOS_THRESHOLD:
            raise NoWorkerAvailableError("All workers are over capacity")

        # Create and save task
        now = datetime.now(UTC)
        task_id = uuid4()
        task = ConversionTask(
            task_id=task_id,
            worker_id=best_worker.worker_id,
            task_type=query.task_type,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        await self._tasks.save_task(task)

        # Increment load as we've "assigned" a resource
        await self._registry.increment_worker_load(best_worker.worker_id)

        return TaskAssignment(
            task_id=task_id,
            sealing_key=best_worker.public_key,
        )
