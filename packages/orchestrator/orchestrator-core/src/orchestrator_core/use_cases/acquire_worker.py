from orchestrator_core.models import WorkerNode
from orchestrator_core.exceptions import NoWorkerAvailableError
from orchestrator_core.ports.incoming.acquire_worker import (
    AcquireWorkerPort,
    AcquireWorkerQuery,
)
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort


class AcquireWorkerUseCase(AcquireWorkerPort):
    DDOS_THRESHOLD = 20

    def __init__(self, registry: WorkerRegistryPort):
        self._registry = registry

    async def __call__(self, query: AcquireWorkerQuery) -> WorkerNode:
        active_workers = await self._registry.get_active_workers(
            query.required_capability
        )

        if not active_workers:
            raise NoWorkerAvailableError(
                f"No active workers with capability '{query.required_capability}'"
            )

        # Sort by load_score (lowest first)
        active_workers.sort(key=lambda w: w.load_score)

        best_worker = active_workers[0]

        if best_worker.load_score >= self.DDOS_THRESHOLD:
            raise NoWorkerAvailableError("All workers are over capacity")

        # Increment load as we've "assigned" a resource
        await self._registry.increment_worker_load(best_worker.worker_id)

        return best_worker
