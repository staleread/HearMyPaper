import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.shared.dependencies.rabbitmq import close_rabbitmq_connection
from app.shared.dependencies.manager import close_manager_client
from app.tts.listener import run_consumer


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Start the consumer in the background
    consumer_task = asyncio.create_task(run_consumer())
    yield
    # Clean up
    consumer_task.cancel()
    await close_rabbitmq_connection()
    await close_manager_client()


app = FastAPI(lifespan=lifespan, title="HearMyPaper TTS Service")
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def check_health() -> str:
    return "I'm good"
