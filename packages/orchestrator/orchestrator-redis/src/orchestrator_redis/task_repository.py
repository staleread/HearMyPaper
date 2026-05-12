from datetime import datetime, UTC
from uuid import UUID
from typing import override
import redis.asyncio as aioredis
from orchestrator_core.models import ConversionTask, TaskStatus
from orchestrator_core.ports.outgoing.task_repository import TaskRepositoryPort


class RedisTaskRepositoryAdapter(TaskRepositoryPort):
    def __init__(self, client: aioredis.Redis):
        self._client = client

    @override
    async def save_task(self, task: ConversionTask) -> None:
        task_id = str(task.task_id)
        task_key = f"task:{task_id}"

        await self._client.hset(
            task_key,
            mapping={
                "task_id": task_id,
                "worker_id": str(task.worker_id),
                "task_type": task.task_type,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
        )

    @override
    async def get_task(self, task_id: UUID) -> ConversionTask | None:
        task_key = f"task:{str(task_id)}"
        data = await self._client.hgetall(task_key)
        if not data:
            return None

        # Helper to handle byte keys from Redis and decode to string
        def get_str(key: str) -> str:
            val = data.get(key.encode(), b"")
            return val.decode() if isinstance(val, bytes) else str(val)

        return ConversionTask(
            task_id=UUID(get_str("task_id")),
            worker_id=UUID(get_str("worker_id")),
            task_type=get_str("task_type"),
            status=TaskStatus(get_str("status")),
            created_at=datetime.fromisoformat(get_str("created_at")),
            updated_at=datetime.fromisoformat(get_str("updated_at")),
        )

    @override
    async def update_task_status(self, task_id: UUID, status: str) -> None:
        task_key = f"task:{str(task_id)}"
        await self._client.hset(
            task_key,
            mapping={
                "status": status,
                "updated_at": datetime.now(UTC).isoformat(),
            },
        )
