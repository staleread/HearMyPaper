import httpx

from .dto import ChallengeRequest, ChallengeResponse, LoginRequest, LoginResponse


class AuthModule:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def create_challenge(self, req: ChallengeRequest) -> ChallengeResponse:
        """Generates a login challenge for the user."""
        response = await self.client.post("/auth/challenge", json=req.model_dump())
        response.raise_for_status()
        return ChallengeResponse.model_validate(response.json())

    async def login(self, req: LoginRequest) -> LoginResponse:
        """Verifies the challenge signature and issues a JWT."""
        response = await self.client.post("/auth/login", json=req.model_dump())
        response.raise_for_status()
        return LoginResponse.model_validate(response.json())
