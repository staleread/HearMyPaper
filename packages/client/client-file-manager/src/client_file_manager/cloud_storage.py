import httpx
from typing import override
from client_core.ports.outgoing.cloud_storage import CloudStoragePort


class CloudStorageAdapter(CloudStoragePort):
    @override
    async def upload(self, url: str, data: bytes) -> None:
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/octet-stream"}
            response = await client.put(url, content=data, headers=headers)
            response.raise_for_status()

    @override
    async def download(self, url: str) -> bytes:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
