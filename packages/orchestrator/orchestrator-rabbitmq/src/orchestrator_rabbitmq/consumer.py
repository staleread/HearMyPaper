import json
from uuid import UUID
from orchestrator_core.ports.incoming.update_task_status import (
    UpdateTaskStatusPort,
    UpdateTaskStatusCommand,
)
from orchestrator_core.models import TaskStatus
from shared_kernel.events import RabbitMQClient
from rodi import Container


class TaskStatusConsumer:
    def __init__(self, client: RabbitMQClient, container: Container):
        self._client = client
        self._container = container

    async def start_consuming(
        self, queue_name: str = "orchestrator.task_status"
    ) -> None:
        await self._client.connect()
        channel = self._client.channel
        exchange = self._client.exchange

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key="task.status.updated")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())

                    cmd = UpdateTaskStatusCommand(
                        task_id=UUID(payload["task_id"]),
                        status=TaskStatus(payload["status"]),
                    )

                    with self._container.provider.create_scope() as scope:
                        update_status = scope.get(UpdateTaskStatusPort)
                        try:
                            await update_status(cmd)
                        except Exception as e:
                            print(f"[ERROR] Failed to update task status: {e}")
                            # message.nack(requeue=True) or move to DLQ
