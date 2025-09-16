from fastapi import APIRouter

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeRequest,
    ChallengeResponse,
    SignatureRequest,
    SignatureResponse,
)
from .service import generate_challenge

router = APIRouter()


@router.post("/register")
async def register(req: RegisterRequest) -> RegisterResponse:
    return RegisterResponse(user_id=1)


@router.post("/challenge")
def request_challenge(req: ChallengeRequest) -> ChallengeResponse:
    challenge = generate_challenge()
    return ChallengeResponse(challenge=challenge)


@router.post("/signature")
def verify_signature(req: SignatureRequest) -> SignatureResponse:
    return SignatureResponse(is_success=True)
