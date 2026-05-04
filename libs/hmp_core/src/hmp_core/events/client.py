from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika


class EventClient:
    """
    Asynchronous RabbitMQ client wrapper using aio-pika.
    Provides a unified interface for publishing and consuming events.
    """
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        """Initializes the robust connection and channel."""
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self.amqp_url)
            self._channel = await self._connection.channel()

    async def declare_exchange(
        self,
        name: str = "hmp.events",
        type: aio_pika.ExchangeType = aio_pika.ExchangeType.TOPIC,
    ) -> aio_pika.abc.AbstractExchange:
        """Declares a durable exchange."""
        await self.connect()
        
        if self._channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")
            
        self._exchange = await self._channel.declare_exchange(
            name, type=type, durable=True
        )
        return self._exchange

    async def publish(
        self, 
        routing_key: str, 
        payload: bytes, 
        correlation_id: str | None = None,
        content_type: str = "application/json"
    ) -> None:
        """Publishes a message to the declared exchange."""
        if self._exchange is None:
            await self.declare_exchange()
            
        if self._exchange is None:
            raise RuntimeError("RabbitMQ exchange is not initialized")
            
        await self._exchange.publish(
            aio_pika.Message(
                body=payload,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type=content_type,
                correlation_id=correlation_id
            ),
            routing_key=routing_key
        )

    async def consume(
        self, 
        queue_name: str, 
        routing_key: str, 
        callback: Callable[[aio_pika.abc.AbstractIncomingMessage], Awaitable[Any]],
        exchange_name: str = "hmp.events"
    ) -> None:
        """Sets up a consumer for a specific queue and routing key."""
        await self.connect()
        
        if self._channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")
            
        # Ensure exchange exists
        exchange = await self.declare_exchange(exchange_name)
        
        # Declare and bind queue
        queue = await self._channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key=routing_key)
        
        # Start consuming
        await queue.consume(callback)

    async def close(self) -> None:
        """Closes the connection safely."""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
            self._channel = None
            self._exchange = None
