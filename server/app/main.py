from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.project.router import router as project_router
from app.audit.router import router as audit_router
from app.pdf_to_audio.router import router as pdf_to_audio_router
from app.submissions.router import router as submission_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")
app.include_router(project_router, prefix="/project")
app.include_router(audit_router, prefix="/audit")
app.include_router(pdf_to_audio_router, prefix="/pdf-to-audio")
app.include_router(submission_router, prefix="/submission", tags=["submission"])


@app.get("/health")
async def check_health() -> str:
    return "I'm good"
