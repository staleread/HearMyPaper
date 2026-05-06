from hmp_core.events import EventClient
from app.shared.config.env import get_env_settings

_event_client: EventClient | None = None


async def get_event_client() -> EventClient:
    global _event_client
    if _event_client is None:
        settings = get_env_settings()
        _event_client = EventClient(settings.rabbitmq_url)
        await _event_client.connect()
    return _event_client


async def close_rabbitmq_connection() -> None:
    global _event_client
    if _event_client:
        await _event_client.close()
        _event_client = None
