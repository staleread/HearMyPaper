import json
from dataclasses import asdict
from datetime import datetime
from typing import Any, cast
from uuid import UUID

import aio_pika


class EventJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


class RabbitMQClient:
    def __init__(self, url: str, exchange_name: str = "hmp.events"):
        self._url = url
        self._exchange_name = exchange_name
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None
        self._exchange: aio_pika.abc.AbstractRobustExchange | None = None

    async def connect(self) -> None:
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._url)
            self._channel = cast(
                aio_pika.abc.AbstractRobustChannel, await self._connection.channel()
            )
            self._exchange = await self._channel.declare_exchange(
                self._exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )

    async def publish(self, routing_key: str, event: Any) -> None:
        await self.connect()
        exchange = self.exchange

        message_body = json.dumps(asdict(event), cls=EventJSONEncoder).encode()
        await exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()

    @property
    def channel(self) -> aio_pika.abc.AbstractRobustChannel:
        if self._channel is None:
            raise RuntimeError("RabbitMQClient is not connected")
        return self._channel

    @property
    def exchange(self) -> aio_pika.abc.AbstractRobustExchange:
        if self._exchange is None:
            raise RuntimeError("RabbitMQClient is not connected")
        return self._exchange
