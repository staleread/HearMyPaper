import base64
from typing import Annotated

from fastapi import APIRouter, Depends

from hmp_manager.domain.auth.models import LoginCommand
from hmp_manager.domain.auth.service import AuthService

from .dependencies import get_auth_service
from .dto import ChallengeRequest, ChallengeResponse, LoginRequest, LoginResponse

router = APIRouter()


@router.post("/challenge", response_model=ChallengeResponse)
async def create_challenge(
    req: ChallengeRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    challenge_bytes = await service.start_login(req.pseudonym)
    challenge_b64 = base64.b64encode(challenge_bytes).decode("utf-8")

    return ChallengeResponse(challenge_b64=challenge_b64)


@router.post("/login", response_model=LoginResponse)
async def execute_login(
    req: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    cmd = LoginCommand(
        pseudonym=req.pseudonym,
        challenge=base64.b64decode(req.challenge_b64),
        signature=base64.b64decode(req.signature_b64),
    )

    auth_token = await service.finalize_login(cmd)

    return LoginResponse(token=auth_token.token)
