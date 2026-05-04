import httpx


async def check_health(client: httpx.AsyncClient, base_url: str) -> str:
    """Checks the health of the manager service."""
    response = await client.get(f"{base_url}/health")
    response.raise_for_status()
    return response.text
