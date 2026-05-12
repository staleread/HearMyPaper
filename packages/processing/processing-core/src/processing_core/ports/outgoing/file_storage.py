from typing import Protocol


class FileStoragePort(Protocol):
    async def generate_upload_url(
        self, file_path: str, ttl_seconds: int = 900
    ) -> str: ...

    async def generate_download_url(
        self, file_path: str, ttl_seconds: int = 3600
    ) -> str: ...

    async def file_exists(self, file_path: str) -> bool: ...
