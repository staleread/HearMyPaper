from httpx import AsyncClient
from datetime import datetime
from shared_kernel.marshal import to_b64, from_b64

from client_core.models import User, AccessLevel
from client_core.ports.outgoing.identity import IdentityPort


class IdentityPortAdapter(IdentityPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_user(self, user_id: str) -> User:
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

    async def get_public_key(self, user_id: str) -> bytes:
        response = await self.client.get(f"/users/{user_id}/public-key")
        response.raise_for_status()
        data = response.json()
        return from_b64(data["public_key_b64"])

    async def init_login(self, user_id: str) -> bytes:
        payload = {"user_id": user_id}
        response = await self.client.post("/auth/challenge", json=payload)
        response.raise_for_status()
        data = response.json()
        return from_b64(data["challenge_b64"])

    async def finalize_login(
        self, user_id: str, challenge: bytes, signature: bytes
    ) -> str:
        payload = {
            "user_id": user_id,
            "challenge_b64": to_b64(challenge),
            "signature_b64": to_b64(signature),
        }
        response = await self.client.post("/auth/login", json=payload)
        response.raise_for_status()
        data = response.json()
        return data["token"]

    async def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        public_key: bytes,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User:
        payload = {
            "name": name,
            "surname": surname,
            "email": email,
            "public_key_b64": to_b64(public_key),
            "confidentiality_level": confidentiality_level.value,
            "integrity_levels": [level.value for level in integrity_levels],
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

    async def update_user(
        self,
        user_id: str,
        name: str,
        surname: str,
        email: str,
        confidentiality_level: AccessLevel,
        integrity_levels: list[AccessLevel],
    ) -> User:
        payload = {
            "name": name,
            "surname": surname,
            "email": email,
            "confidentiality_level": confidentiality_level.value,
            "integrity_levels": [level.value for level in integrity_levels],
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
