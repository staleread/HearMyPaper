import aioboto3
from contextlib import asynccontextmanager
from typing import AsyncGenerator, TYPE_CHECKING

if TYPE_CHECKING:
    from types_aiobotocore_s3.client import S3Client
else:
    S3Client = object

class StorageClient:
    """
    Asynchronous S3/MinIO client wrapper using aioboto3.
    Supports the 'Claim Check' pattern by allowing secure file 
    upload and download from object storage.
    """
    def __init__(
        self, 
        endpoint_url: str, 
        access_key: str, 
        secret_key: str, 
        region_name: str = "us-east-1"
    ):
        self.session = aioboto3.Session()
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[S3Client, None]:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as client:
            yield client

    async def upload_file(self, bucket: str, key: str, data: bytes) -> None:
        """Uploads raw bytes to a specific bucket and key."""
        async with self._get_client() as client:
            await client.put_object(Bucket=bucket, Key=key, Body=data)

    async def download_file(self, bucket: str, key: str) -> bytes:
        """Downloads raw bytes from a specific bucket and key."""
        async with self._get_client() as client:
            response = await client.get_object(Bucket=bucket, Key=key)
            async with response["Body"] as stream:
                return await stream.read()

    async def ensure_bucket(self, bucket: str) -> None:
        """Ensures that the specified bucket exists."""
        async with self._get_client() as client:
            try:
                await client.head_bucket(Bucket=bucket)
            except Exception:
                await client.create_bucket(Bucket=bucket)

    async def get_presigned_upload_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        """
        Generates a pre-signed URL for uploading a file (PUT).
        Ensures the Manager defines the exact location, preventing unauthorized writes.
        """
        async with self._get_client() as client:
            return await client.generate_presigned_url(
                ClientMethod="put_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )

    async def get_presigned_download_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        """
        Generates a short-lived pre-signed URL for downloading a file (GET).
        Follows the Principle of Least Privilege.
        """
        async with self._get_client() as client:
            return await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )
