from fastapi import FastAPI

from app.auth.router import router as auth_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")


@app.get("/health")
async def check_health():
    return "I'm good"
