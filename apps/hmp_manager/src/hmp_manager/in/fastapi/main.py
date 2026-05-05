from fastapi import FastAPI
from contextlib import asynccontextmanager
from .dependencies import get_redis_service, get_postgres_engine

from .auth.routes import router as auth_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield

    # Shutdown logic
    await get_postgres_engine().disconnect()
    await get_redis_service().close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
