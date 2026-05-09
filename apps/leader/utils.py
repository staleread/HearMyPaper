from typing import cast
from blacksheep import Application, Request
from blacksheep.server.di import register_http_context
from redis.asyncio import Redis
from rodi import ActivationScope, Container
from shared_kernel.storage import PostgresClient, RedisClient
from sqlalchemy.ext.asyncio import AsyncSession


def use_postgres(app: Application, url: str):
    postgres_client = PostgresClient(url, echo=True)

    # Enable Request injection and create a DI scope for every request
    register_http_context(app)

    async def database_middleware(request: Request, next_handler):
        async with postgres_client.transactional_session() as session:
            # Seed the session into the request's DI scope.
            # register_http_context() ensures request._di_scope exists.
            request._di_scope.scoped_services[AsyncSession] = session  # ty:ignore[unresolved-attribute]

            return await next_handler(request)

    app.middlewares.append(database_middleware)

    def session_factory(context: ActivationScope) -> AsyncSession:
        """
        Factory to resolve the AsyncSession from the current DI scope.
        The session is seeded into the scope by the database middleware.
        """
        return context.scoped_services[AsyncSession]  # ty:ignore[invalid-argument-type, invalid-return-type, not-subscriptable]

    (
        cast(Container, app.services)
        .add_instance(postgres_client, PostgresClient)
        .add_scoped_by_factory(session_factory)
    )

    async def dispose_postgres(_: Application):
        await postgres_client.dispose()

    app.on_stop += dispose_postgres


def use_redis(app: Application, url: str):
    redis_client = RedisClient(url)

    cast(Container, app.services).add_instance(redis_client.client, Redis)

    async def dispose_redis(_: Application):
        await redis_client.close()

    app.on_stop += dispose_redis
