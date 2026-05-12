from typing import Protocol


class StoragePort(Protocol):
    async def generate_upload_url(
        self, path: str, content_type: str | None = None, ttl_seconds: int = 3600
    ) -> str: ...

    async def generate_download_url(
        self, path: str, ttl_seconds: int = 3600
    ) -> str: ...

    async def file_exists(self, path: str) -> bool: ...
