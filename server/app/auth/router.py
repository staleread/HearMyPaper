from fastapi import APIRouter

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeRequest,
    ChallengeResponse,
    SignatureRequest,
    SignatureResponse,
)

router = APIRouter()


@router.post("/register")
async def register(req: RegisterRequest) -> RegisterResponse:
    return RegisterResponse(user_id=1)


@router.post("/challenge")
def request_challenge(req: ChallengeRequest) -> ChallengeResponse:
    return ChallengeResponse(challenge="K3d9jr_Mock_challenge_.wsKsdf")


@router.post("/signature")
def verify_signature(req: SignatureRequest) -> SignatureResponse:
    return SignatureResponse(is_success=True)
