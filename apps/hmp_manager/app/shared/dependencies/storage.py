from hmp_core.storage.client import StorageClient
from app.shared.config.env import get_env_settings

_storage_client: StorageClient | None = None

def get_storage_client() -> StorageClient:
    global _storage_client
    if _storage_client is None:
        settings = get_env_settings()
        _storage_client = StorageClient(
            endpoint_url=settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
        )
    return _storage_client
