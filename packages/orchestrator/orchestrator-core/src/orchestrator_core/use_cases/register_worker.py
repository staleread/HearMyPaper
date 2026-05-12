from orchestrator_core.models import WorkerNode
from orchestrator_core.ports.incoming.register_worker import (
    RegisterWorkerPort,
    RegisterWorkerCommand,
)
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort


class RegisterWorkerUseCase(RegisterWorkerPort):
    def __init__(self, registry: WorkerRegistryPort):
        self._registry = registry

    async def __call__(self, cmd: RegisterWorkerCommand) -> None:
        print(
            f"[DEBUG] Executing RegisterWorkerUseCase for worker {cmd.worker_id} with capabilities {cmd.capabilities}"
        )
        worker = WorkerNode(
            worker_id=cmd.worker_id,
            public_key=cmd.public_key,
            load_score=0,
            capabilities=cmd.capabilities,
        )
        await self._registry.save_worker(worker)
