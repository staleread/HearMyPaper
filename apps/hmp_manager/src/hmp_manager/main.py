from fastapi import FastAPI
from contextlib import asynccontextmanager

from .dependencies import (
    get_redis_service,
    get_postgres_engine,
)
from .identity.adapters.driving.fastapi import router as identity_router
from .education.adapters.driving.fastapi import router as education_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield

    # Shutdown logic
    await get_postgres_engine().disconnect()
    await get_redis_service().close()


app = FastAPI(lifespan=lifespan)
app.include_router(identity_router, prefix="/api/v1", tags=["identity"])
app.include_router(education_router, prefix="/api/v1", tags=["education"])
