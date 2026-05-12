import json
from uuid import UUID
from shared_kernel.events import RabbitMQClient
from shared_kernel.storage import PostgresClient
from sqlalchemy.ext.asyncio import AsyncSession
from processing_core.ports.incoming.update_conversion_status import (
    UpdateConversionStatusPort,
)
from rodi import Container


class ProcessingStatusConsumer:
    def __init__(
        self,
        rabbit_client: RabbitMQClient,
        container: Container,
        postgres_client: PostgresClient,
    ):
        self._rabbit_client = rabbit_client
        self._container = container
        self._postgres_client = postgres_client

    async def start_listening(self):
        await self._rabbit_client.connect()
        channel = self._rabbit_client.channel
        exchange = self._rabbit_client.exchange

        queue = await channel.declare_queue("processing.status.updates", durable=True)
        await queue.bind(exchange, routing_key="task.status.updated")

        print("[INFO] Processing module listening for status updates...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())
                    task_id = UUID(payload["task_id"])
                    status = payload["status"]

                    print(
                        f"[INFO] Updating conversion status for task {task_id} to {status}"
                    )

                    with self._container.provider.create_scope() as scope:
                        async with (
                            self._postgres_client.transactional_session() as session
                        ):
                            scope.scoped_services[AsyncSession] = session
                            update_status = scope.get(UpdateConversionStatusPort)

                            try:
                                await update_status(task_id, status)
                            except Exception as e:
                                print(
                                    f"[ERROR] Failed to update conversion status: {e}"
                                )
