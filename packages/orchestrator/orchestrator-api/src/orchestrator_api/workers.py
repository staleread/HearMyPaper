from blacksheep import FromJSON
from blacksheep.server.controllers import Controller, post
from blacksheep.server.responses import ok
from pydantic import BaseModel
from uuid import UUID
from orchestrator_core.ports.incoming.register_worker import (
    RegisterWorkerPort,
    RegisterWorkerCommand,
)
from shared_kernel.marshal import from_b64


class HeartbeatRequest(BaseModel):
    worker_id: UUID
    public_key_b64: str
    capabilities: list[str]


class Workers(Controller):
    @classmethod
    def route(cls) -> str | None:
        return "/orchestrator/workers"

    def __init__(self, register_worker_port: RegisterWorkerPort) -> None:
        self.register_worker_port = register_worker_port

    @post("/heartbeat")
    async def heartbeat(self, data: FromJSON[HeartbeatRequest]):
        """
        Register or update a worker's heartbeat and capabilities.
        """
        req = data.value
        cmd = RegisterWorkerCommand(
            worker_id=req.worker_id,
            public_key=from_b64(req.public_key_b64),
            capabilities=req.capabilities,
        )
        await self.register_worker_port(cmd)
        return ok()
