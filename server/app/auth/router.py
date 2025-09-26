from fastapi import APIRouter

from app.shared.dependencies.db import PostgresConnectionDep

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)
from . import service as auth_service


router = APIRouter()


@router.post("/register")
async def register(
    req: RegisterRequest, connection: PostgresConnectionDep
) -> RegisterResponse:
    return auth_service.register_user(req, connection=connection)


@router.post("/challenge")
async def request_challenge(req: ChallengeRequest) -> ChallengeResponse:
    return auth_service.create_login_challenge()


@router.post("/signature")
async def login(req: LoginRequest, connection: PostgresConnectionDep) -> LoginResponse:
    return auth_service.login_user(req, connection=connection)
