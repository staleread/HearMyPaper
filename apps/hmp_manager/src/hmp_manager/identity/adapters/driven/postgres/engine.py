from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class PostgresEngine:
    def __init__(self, connection_url: str):
        self.engine = create_async_engine(connection_url)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            async with session.begin():
                yield session

    async def disconnect(self):
        await self.engine.dispose()
