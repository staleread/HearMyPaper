from datetime import datetime, UTC
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
        worker = WorkerNode(
            worker_id=cmd.worker_id,
            public_key=cmd.public_key,
            last_heartbeat=datetime.now(UTC),
            load_score=0,  # Initialize or keep existing load?
            # For simplicity, we'll assume the registry handles persistence of load if it exists,
            # but for a new registration or heartbeat, we mostly care about liveness and keys.
            capabilities=cmd.capabilities,
        )
        await self._registry.save_worker(worker)
