import httpx

from .dto import ChallengeRequest, ChallengeResponse, LoginRequest, LoginResponse


async def create_challenge(
    client: httpx.AsyncClient, base_url: str, req: ChallengeRequest
) -> ChallengeResponse:
    """Generates a login challenge for the user."""
    response = await client.post(f"{base_url}/auth/challenge", json=req.model_dump())
    response.raise_for_status()
    return ChallengeResponse.model_validate(response.json())


async def login(
    client: httpx.AsyncClient, base_url: str, req: LoginRequest
) -> LoginResponse:
    """Verifies the challenge signature and issues a JWT."""
    response = await client.post(f"{base_url}/auth/login", json=req.model_dump())
    response.raise_for_status()
    return LoginResponse.model_validate(response.json())
