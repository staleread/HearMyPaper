from fastapi import APIRouter, HTTPException
from hmp_core.utils import to_b64, from_b64

from hmp_manager.identity.domain.models import LoginCommand
from hmp_manager.identity.domain.exceptions import (
    UserNotFoundError,
    InvalidChallengeError,
    AuthenticationFailedError,
)

from .dependencies import AuthServiceDep
from .dto import (
    ChallengeRequest,
    ChallengeResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter()


@router.post("/challenge", response_model=ChallengeResponse)
async def create_challenge(
    req: ChallengeRequest,
    service: AuthServiceDep,
):
    try:
        challenge_bytes = await service.start_login(req.id)
        return ChallengeResponse(challenge_b64=to_b64(challenge_bytes))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def execute_login(
    req: LoginRequest,
    service: AuthServiceDep,
):
    cmd = LoginCommand(
        id=req.id,
        challenge=from_b64(req.challenge_b64),
        signature=from_b64(req.signature_b64),
    )

    try:
        auth_token = await service.finalize_login(cmd)
        return LoginResponse(token=auth_token.token)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidChallengeError, AuthenticationFailedError:
        raise HTTPException(
            status_code=401,
            detail="Invalid challenge or signature",
        )
