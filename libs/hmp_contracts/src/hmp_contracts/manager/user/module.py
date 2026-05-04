import httpx

from .dto import UserCreateRequest, UserResponse, UserUpdateRequest


class UserModule:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def create(self, req: UserCreateRequest) -> UserResponse:
        """Creates a new user and generates their stable pseudonym."""
        response = await self.client.post("/users/", json=req.model_dump())
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    async def get(self, pseudonym: str) -> UserResponse:
        """Retrieves user details by pseudonym."""
        response = await self.client.get(f"/users/{pseudonym}")
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    async def update(self, pseudonym: str, req: UserUpdateRequest) -> UserResponse:
        """Updates user details by pseudonym."""
        response = await self.client.put(f"/users/{pseudonym}", json=req.model_dump())
        response.raise_for_status()
        return UserResponse.model_validate(response.json())

    async def get_public_key(self, pseudonym: str) -> dict:
        """Returns the public key for a given user pseudonym."""
        response = await self.client.get(f"/users/{pseudonym}/public-key")
        response.raise_for_status()
        return response.json()
