from typing import Protocol


class CloudStoragePort(Protocol):
    async def upload(self, url: str, data: bytes) -> None:
        """Uploads raw bytes to the given pre-signed URL."""
        ...

    async def download(self, url: str) -> bytes:
        """Downloads raw bytes from the given pre-signed URL."""
        ...
