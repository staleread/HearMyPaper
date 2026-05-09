from typing import Protocol


class StoragePort(Protocol):
    async def generate_upload_url(self, path: str, ttl_seconds: int = 3600) -> str: ...
    async def generate_download_url(
        self, path: str, ttl_seconds: int = 3600
    ) -> str: ...
