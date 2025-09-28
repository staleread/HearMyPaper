from fastapi import APIRouter

from app.shared.dependencies.db import PostgresRunnerDep

from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from . import service as auth_service


router = APIRouter()


@router.post("/challenge")
async def get_login_challenge(req: ChallengeRequest) -> ChallengeResponse:
    return auth_service.create_login_challenge()


@router.post("/login")
async def login_user(req: LoginRequest, db: PostgresRunnerDep) -> LoginResponse:
    return auth_service.login_user(req, db=db)
