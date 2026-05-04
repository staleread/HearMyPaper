from hmp_core.storage import ObjectStorageClient
from app.shared.config.env import get_env_settings

_storage_client: ObjectStorageClient | None = None

def get_storage_client() -> ObjectStorageClient:
    global _storage_client
    if _storage_client is None:
        settings = get_env_settings()
        _storage_client = ObjectStorageClient(
            endpoint_url=settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
        )
    return _storage_client
