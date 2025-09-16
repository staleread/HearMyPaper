from fastapi import APIRouter

from .models import (
    RegisterRequest,
    RegisterResponse,
    ChallengeRequest,
    ChallengeResponse,
    SignatureRequest,
    SignatureResponse,
)
from .service import generate_challenge, verify_signed_challenge

router = APIRouter()

public_keys = dict()


@router.post("/register")
async def register(req: RegisterRequest) -> RegisterResponse:
    user_id = 1
    public_keys[user_id] = req.public_key

    return RegisterResponse(user_id=user_id)


@router.post("/challenge")
async def request_challenge(req: ChallengeRequest) -> ChallengeResponse:
    challenge = generate_challenge()
    return ChallengeResponse(challenge=challenge)


@router.post("/signature")
async def verify_challenge(req: SignatureRequest) -> SignatureResponse:
    public_key_b64 = public_keys[req.user_id]
    is_success = verify_signed_challenge(
        signature_b64=req.signature,
        challenge_b64=req.challenge,
        public_key_b64=public_key_b64,
    )

    return SignatureResponse(is_success=is_success)
