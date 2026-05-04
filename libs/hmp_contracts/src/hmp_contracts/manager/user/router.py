import httpx

from .dto import UserCreateRequest, UserResponse, UserUpdateRequest


async def create_user(
    client: httpx.AsyncClient, base_url: str, req: UserCreateRequest
) -> UserResponse:
    """Creates a new user and generates their stable pseudonym."""
    response = await client.post(f"{base_url}/users/", json=req.model_dump())
    response.raise_for_status()
    return UserResponse.model_validate(response.json())


async def get_user(
    client: httpx.AsyncClient, base_url: str, pseudonym: str
) -> UserResponse:
    """Retrieves user details by pseudonym."""
    response = await client.get(f"{base_url}/users/{pseudonym}")
    response.raise_for_status()
    return UserResponse.model_validate(response.json())


async def update_user(
    client: httpx.AsyncClient, base_url: str, pseudonym: str, req: UserUpdateRequest
) -> UserResponse:
    """Updates user details by pseudonym."""
    response = await client.put(f"{base_url}/users/{pseudonym}", json=req.model_dump())
    response.raise_for_status()
    return UserResponse.model_validate(response.json())


async def get_public_key(
    client: httpx.AsyncClient, base_url: str, pseudonym: str
) -> dict:
    """Returns the public key for a given user pseudonym."""
    response = await client.get(f"{base_url}/users/{pseudonym}/public-key")
    response.raise_for_status()
    return response.json()
