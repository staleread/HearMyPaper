from orchestrator_core.ports.incoming.heartbeat import (
    HeartbeatPort,
    HeartbeatCommand,
)
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort


class HeartbeatUseCase(HeartbeatPort):
    def __init__(self, registry: WorkerRegistryPort):
        self._registry = registry

    async def __call__(self, cmd: HeartbeatCommand) -> None:
        await self._registry.heartbeat(cmd.worker_id)
