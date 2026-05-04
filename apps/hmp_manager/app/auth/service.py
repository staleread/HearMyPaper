from fastapi import HTTPException
from redis import asyncio as aioredis
from hmp_core.storage import SqlRunner
from .dto import ChallengeRequest, ChallengeResponse, LoginRequest, LoginResponse
from . import utils
from app.user import repository as user_repo


async def create_challenge(
    req: ChallengeRequest, redis: aioredis.Redis, db: SqlRunner
) -> ChallengeResponse:
    # Verify user exists
    user = user_repo.get_user_by_pseudonym(req.pseudonym, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    challenge = utils.generate_challenge()
    # Store challenge in redis with 5-minute TTL
    await redis.set(f"challenge:{req.pseudonym}", challenge, ex=300)

    return ChallengeResponse(challenge=challenge)


async def login(
    req: LoginRequest, redis: aioredis.Redis, db: SqlRunner
) -> LoginResponse:
    # Retrieve stored challenge
    stored_challenge = await redis.get(f"challenge:{req.pseudonym}")
    if not stored_challenge or stored_challenge != req.challenge:
        raise HTTPException(status_code=400, detail="Invalid or expired challenge")

    # Retrieve user public key
    public_key = user_repo.get_public_key_by_pseudonym(req.pseudonym, db=db)
    if not public_key:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify signature
    is_valid = utils.verify_challenge(req.signature, req.challenge, public_key)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Delete challenge after successful use
    await redis.delete(f"challenge:{req.pseudonym}")

    # Fetch user full data for claims
    user = user_repo.get_user_by_pseudonym(req.pseudonym, db=db)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found during claim resolution"
        )

    # Create JWT
    token = utils.create_access_token(
        {
            "sub": user["pseudonym"],
            "confidentiality_level": user["confidentiality_level"],
            "integrity_levels": user["integrity_levels"],
            "workload_id": "spiffe://hmp.internal/user",  # Generic for human users
        }
    )

    return LoginResponse(token=token)
