from typing import override
from shared_kernel.storage import ObjectStorageClient
from submissions_core.ports.outgoing.storage import StoragePort


class S3StorageAdapter(StoragePort):
    def __init__(self, storage_client: ObjectStorageClient, bucket: str):
        self._storage_client = storage_client
        self._bucket = bucket

    @override
    async def generate_upload_url(self, path: str, ttl_seconds: int = 3600) -> str:
        params = {"Bucket": self._bucket, "Key": path}
        if path.endswith(".bin"):
            params["ContentType"] = "application/octet-stream"

        async for client in self._storage_client.get_signing_client():
            return await client.generate_presigned_url(
                ClientMethod="put_object",
                Params=params,
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")

    @override
    async def generate_download_url(self, path: str, ttl_seconds: int = 3600) -> str:
        async for client in self._storage_client.get_signing_client():
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket, "Key": path},
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")
