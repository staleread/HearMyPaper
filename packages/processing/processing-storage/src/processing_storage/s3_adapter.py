from typing import override
from botocore.exceptions import ClientError
from shared_kernel.storage import ObjectStorageClient
from processing_core.ports.outgoing.storage import StoragePort


class S3StorageAdapter(StoragePort):
    def __init__(self, storage_client: ObjectStorageClient, bucket: str):
        self._storage_client = storage_client
        self._bucket = bucket

    @override
    async def generate_upload_url(
        self, path: str, content_type: str | None = None, ttl_seconds: int = 900
    ) -> str:
        params = {"Bucket": self._bucket, "Key": path}
        if content_type:
            params["ContentType"] = content_type

        async for client in self._storage_client.get_client():
            return await client.generate_presigned_url(
                ClientMethod="put_object",
                Params=params,
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")

    @override
    async def generate_download_url(self, path: str, ttl_seconds: int = 900) -> str:
        async for client in self._storage_client.get_client():
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket, "Key": path},
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")

    @override
    async def file_exists(self, path: str) -> bool:
        async for client in self._storage_client.get_client():
            try:
                await client.head_object(Bucket=self._bucket, Key=path)
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    return False
                raise
        raise RuntimeError("Failed to acquire S3 client")
