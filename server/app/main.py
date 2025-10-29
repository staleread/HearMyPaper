import base64
from fastapi import FastAPI, HTTPException

from app.auth.router import router as auth_router
from app.project.router import router as project_router
from app.audit.router import router as audit_router
from app.pdf_to_audio.router import router as pdf_to_audio_router
from app.submission.router import router as submission_router
from app.shared.config.env import env_settings
from app.shared.utils.crypto import load_server_private_key

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(project_router, prefix="/project", tags=["project"])
app.include_router(audit_router, prefix="/audit", tags=["audit"])
app.include_router(pdf_to_audio_router, prefix="/pdf-to-audio", tags=["pdf-to-audio"])
app.include_router(submission_router, prefix="/submission", tags=["submission"])


@app.get("/health")
async def check_health() -> str:
    return "I'm good"


@app.get("/public-key")
async def get_public_key() -> dict[str, str]:
    """Return the server's public key for encrypting data."""
    try:
        private_key = load_server_private_key(env_settings.server_private_key_password)
        public_key_bytes = private_key.public_key().public_bytes_raw()
        return {"public_key": base64.b64encode(public_key_bytes).decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load public key")
