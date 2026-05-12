import json
from uuid import UUID
from typing import override
import redis.asyncio as aioredis
from orchestrator_core.models import WorkerNode
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort


class RedisWorkerRegistryAdapter(WorkerRegistryPort):
    HEARTBEAT_TTL = 30  # seconds

    def __init__(self, client: aioredis.Redis):
        self._client = client

    @override
    async def save_worker(self, worker: WorkerNode) -> None:
        worker_id = str(worker.worker_id)
        worker_key = f"worker:{worker_id}"
        heartbeat_key = f"worker_heartbeat:{worker_id}"

        # Get existing load if it exists
        existing_load = await self._client.hget(worker_key, "load_score")
        load_score = int(existing_load) if existing_load else worker.load_score

        # Save worker metadata
        await self._client.hset(
            worker_key,
            mapping={
                "worker_id": worker_id,
                "public_key": worker.public_key,
                "load_score": str(load_score),
                "capabilities": json.dumps(worker.capabilities),
            },
        )

        # Set liveness key
        await self._client.setex(heartbeat_key, self.HEARTBEAT_TTL, "alive")

        # Update ZSET for load balancing
        await self._client.zadd("worker_load", {worker_id: load_score})

        # Update capability sets
        for capability in worker.capabilities:
            await self._client.sadd(f"capability:{capability}", worker_id)

    @override
    async def heartbeat(self, worker_id: UUID) -> None:
        heartbeat_key = f"worker_heartbeat:{str(worker_id)}"
        await self._client.expire(heartbeat_key, self.HEARTBEAT_TTL)

    @override
    async def get_active_workers(self, required_capability: str) -> list[WorkerNode]:
        capability_key = f"capability:{required_capability}"
        worker_ids_bytes = await self._client.smembers(capability_key)

        active_workers = []
        for wid_bytes in worker_ids_bytes:
            wid = wid_bytes.decode()
            if not await self._client.exists(f"worker_heartbeat:{wid}"):
                continue

            data = await self._client.hgetall(f"worker:{wid}")
            if not data:
                continue

            def get_val(key: str) -> bytes:
                return data.get(key.encode(), b"")

            active_workers.append(
                WorkerNode(
                    worker_id=UUID(wid),
                    public_key=get_val("public_key"),
                    load_score=int(get_val("load_score").decode()),
                    capabilities=json.loads(get_val("capabilities").decode()),
                )
            )

        return active_workers

    @override
    async def increment_worker_load(self, worker_id: UUID) -> None:
        wid = str(worker_id)
        await self._client.hincrby(f"worker:{wid}", "load_score", 1)
        await self._client.zincrby("worker_load", 1, wid)

    @override
    async def decrement_worker_load(self, worker_id: UUID) -> None:
        wid = str(worker_id)
        current_load_str = await self._client.hget(f"worker:{wid}", "load_score")
        if current_load_str:
            current_load = int(current_load_str)
            if current_load > 0:
                await self._client.hincrby(f"worker:{wid}", "load_score", -1)
                await self._client.zincrby("worker_load", -1, wid)
            else:
                await self._client.hset(f"worker:{wid}", "load_score", "0")
                await self._client.zadd("worker_load", {wid: 0})
