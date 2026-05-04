import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth.router import router as auth_router
from app.project.router import router as project_router
from app.audit.router import router as audit_router
from app.submission.router import router as submission_router
from app.admin.router import router as admin_router
from app.conversion.router import router as conversion_router
from app.user.router import router as user_router
from app.shared.config.env import get_env_settings
from app.shared.dependencies.rabbitmq import close_rabbitmq_connection
from app.conversion.listener import run_result_consumer


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 1. Redis Cache Initialization
    redis = aioredis.from_url(
        get_env_settings().redis_url, encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    # 2. Start Background RabbitMQ Consumer for Conversion Results
    result_task = asyncio.create_task(run_result_consumer())

    yield

    # 3. Shutdown Cleanup
    result_task.cancel()
    await close_rabbitmq_connection()


app = FastAPI(lifespan=lifespan, title="HearMyPaper API")
Instrumentator().instrument(app).expose(app)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(project_router, prefix="/project", tags=["project"])
app.include_router(audit_router, prefix="/audit", tags=["audit"])
app.include_router(submission_router, prefix="/submission", tags=["submission"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(conversion_router, prefix="/conversions", tags=["conversion"])
app.include_router(user_router, prefix="/users", tags=["user"])


@app.get("/health")
async def check_health() -> str:
    return "I'm good"
