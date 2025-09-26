from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.user.router import router as user_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")


@app.get("/health")
async def check_health():
    return "I'm good"
