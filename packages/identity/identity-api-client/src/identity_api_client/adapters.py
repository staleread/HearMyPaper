from httpx import AsyncClient
from datetime import datetime
from typing import override
from shared_kernel.marshal import to_b64, from_b64

from identity_core.models import User
from identity_core.enums import AccessLevel
from identity_core.ports.incoming import (
    AuthToken,
    GetUserPort,
    CreateUserPort,
    UpdateUserPort,
    GetUserPublicKeyPort,
    InitLoginPort,
    FinalizeLoginPort,
    UserCreateCommand,
    UserUpdateCommand,
    LoginCommand,
)


class GetUserByIdAdapter(GetUserPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, user_id: str) -> User:
        response = await self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        data = response.json()
        return User(
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            confidentiality_level=AccessLevel(data["confidentiality_level"]),
            integrity_levels=[AccessLevel(level) for level in data["integrity_levels"]],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class CreateUserAdapter(CreateUserPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: UserCreateCommand) -> User:
        payload = {
            "name": cmd.name,
            "surname": cmd.surname,
            "email": cmd.email,
            "public_key_b64": to_b64(cmd.public_key),
            "confidentiality_level": cmd.confidentiality_level.value,
            "integrity_levels": [level.value for level in cmd.integrity_levels],
        }
        response = await self.client.post("/users/", json=payload)
        response.raise_for_status()
        data = response.json()
        return User(
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            confidentiality_level=AccessLevel(data["confidentiality_level"]),
            integrity_levels=[AccessLevel(level) for level in data["integrity_levels"]],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class UpdateUserAdapter(UpdateUserPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, user_id: str, cmd: UserUpdateCommand) -> User:
        payload = {
            "name": cmd.name,
            "surname": cmd.surname,
            "email": cmd.email,
            "confidentiality_level": cmd.confidentiality_level.value,
            "integrity_levels": [level.value for level in cmd.integrity_levels],
        }
        response = await self.client.put(f"/users/{user_id}", json=payload)
        response.raise_for_status()
        data = response.json()
        return User(
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            confidentiality_level=AccessLevel(data["confidentiality_level"]),
            integrity_levels=[AccessLevel(level) for level in data["integrity_levels"]],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class GetUserPublicKeyAdapter(GetUserPublicKeyPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, user_id: str) -> bytes:
        response = await self.client.get(f"/users/{user_id}/public-key")
        response.raise_for_status()
        data = response.json()
        return from_b64(data["public_key_b64"])


class InitLoginAdapter(InitLoginPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, user_id: str) -> bytes:
        payload = {"user_id": user_id}
        response = await self.client.post("/auth/challenge", json=payload)
        response.raise_for_status()
        data = response.json()
        return from_b64(data["challenge_b64"])


class FinalizeLoginAdapter(FinalizeLoginPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    @override
    async def __call__(self, cmd: LoginCommand) -> AuthToken:
        payload = {
            "user_id": cmd.user_id,
            "challenge_b64": to_b64(cmd.challenge),
            "signature_b64": to_b64(cmd.signature),
        }
        response = await self.client.post("/auth/login", json=payload)
        response.raise_for_status()
        data = response.json()
        return AuthToken(
            token=data["token"], expires_at=datetime.fromisoformat(data["expires_at"])
        )
