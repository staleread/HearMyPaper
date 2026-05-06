from fastapi import FastAPI
from contextlib import asynccontextmanager

from hmp_manager.driving.fastapi.dependencies import (
    get_redis_service,
    get_postgres_engine,
)
from .auth import router as auth_router
from .user import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield

    # Shutdown logic
    await get_postgres_engine().disconnect()
    await get_redis_service().close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
