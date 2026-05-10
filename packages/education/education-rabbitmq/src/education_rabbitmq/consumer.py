import json
from datetime import datetime
from uuid import UUID

from education_core.ports.incoming.register_attempt import (
    RegisterAttemptPort,
    RegisterAttemptCommand,
)
from shared_kernel.events import RabbitMQClient
from shared_kernel.storage import PostgresClient
from sqlalchemy.ext.asyncio import AsyncSession
from rodi import Container


class RabbitMQEventConsumer:
    def __init__(
        self,
        client: RabbitMQClient,
        container: Container,
        postgres_client: PostgresClient,
    ):
        self._client = client
        self._container = container
        self._postgres_client = postgres_client

    async def start_consuming(
        self, queue_name: str = "education.submission_committed"
    ) -> None:
        await self._client.connect()
        channel = self._client.channel
        exchange = self._client.exchange

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key="submission.committed")

        print(f"[INFO] Started consuming from {queue_name}")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode())

                    cmd = RegisterAttemptCommand(
                        submission_id=UUID(payload["submission_id"]),
                        student_id=payload["student_id"],
                        project_id=UUID(payload["project_id"]),
                        timestamp=datetime.fromisoformat(payload["timestamp"]),
                    )

                    # Create a new scope for each message to handle scoped dependencies (like DB session)
                    with self._container.provider.create_scope() as scope:
                        async with (
                            self._postgres_client.transactional_session() as session
                        ):
                            scope.scoped_services[AsyncSession] = session

                            register_attempt = scope.get(RegisterAttemptPort)

                            try:
                                await register_attempt(cmd)
                            except Exception as e:
                                print(f"[ERROR] Failed to register attempt: {e}")
                                # In a real system, you might want to retry or move to DLQ
