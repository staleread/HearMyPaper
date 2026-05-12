from typing import override
from shared_kernel.storage import ObjectStorageClient
from processing_core.ports.outgoing.file_storage import FileStoragePort


class S3StorageAdapter(FileStoragePort):
    def __init__(self, storage_client: ObjectStorageClient, bucket: str):
        self._storage_client = storage_client
        self._bucket = bucket

    @override
    async def generate_upload_url(self, file_path: str, ttl_seconds: int = 900) -> str:
        async for client in self._storage_client.get_client():
            return await client.generate_presigned_url(
                ClientMethod="put_object",
                Params={"Bucket": self._bucket, "Key": file_path},
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")

    @override
    async def generate_download_url(
        self, file_path: str, ttl_seconds: int = 3600
    ) -> str:
        async for client in self._storage_client.get_client():
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self._bucket, "Key": file_path},
                ExpiresIn=ttl_seconds,
            )
        raise RuntimeError("Failed to acquire S3 client")

    @override
    async def file_exists(self, file_path: str) -> bool:
        async for client in self._storage_client.get_client():
            try:
                await client.head_object(Bucket=self._bucket, Key=file_path)
                return True
            except Exception as e:
                if "404" in str(e):
                    return False
                raise RuntimeError(f"Failed to check file existence: {e}") from e
        raise RuntimeError("Failed to acquire S3 client")
