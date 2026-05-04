import base64

import httpx


class HmpManagerClient:
    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self.base_url = base_url
        self.client = http_client

    async def get_public_key(self, identifier: str) -> bytes:
        """Fetches a user's public key for Sealed Box finalization."""
        response = await self.client.get(
            f"{self.base_url}/users/{identifier}/public-key"
        )
        response.raise_for_status()
        data = response.json()
        return base64.b64decode(data["public_key"])
