from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.user.router import router as user_router
from app.project.router import router as project_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(project_router, prefix="/project")


@app.get("/health")
async def check_health() -> str:
    return "I'm good"
