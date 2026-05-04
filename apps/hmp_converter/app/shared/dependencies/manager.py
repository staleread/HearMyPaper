import httpx
from hmp_core.clients import HmpManagerClient
from app.shared.config.env import get_env_settings

_manager_client: HmpManagerClient | None = None
_http_client: httpx.AsyncClient | None = None


async def get_manager_client() -> HmpManagerClient:
    global _manager_client, _http_client
    if _manager_client is None:
        settings = get_env_settings()
        _http_client = httpx.AsyncClient()
        _manager_client = HmpManagerClient(settings.manager_url, _http_client)
    return _manager_client


async def close_manager_client() -> None:
    global _manager_client, _http_client
    if _http_client:
        await _http_client.aclose()
        _http_client = None
        _manager_client = None
