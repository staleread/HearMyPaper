from collections.abc import AsyncGenerator
from typing import Any

import aioboto3


class ObjectStorageClient:
    """
    Asynchronous S3/MinIO client manager using aioboto3.
    """

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region_name: str = "us-east-1",
    ):
        self.session = aioboto3.Session()
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name

    async def get_client(self) -> AsyncGenerator[Any, None]:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        ) as client:
            yield client


class ObjectStorageRunner:
    """
    Runner wrapping an existing aioboto3 S3 client.
    """

    def __init__(self, client: Any):
        self.client = client

    async def upload_file(self, bucket: str, key: str, data: bytes) -> None:
        await self.client.put_object(Bucket=bucket, Key=key, Body=data)

    async def download_file(self, bucket: str, key: str) -> bytes:
        response = await self.client.get_object(Bucket=bucket, Key=key)
        async with response["Body"] as stream:
            return await stream.read()

    async def ensure_bucket(self, bucket: str) -> None:
        try:
            await self.client.head_bucket(Bucket=bucket)
        except Exception:
            await self.client.create_bucket(Bucket=bucket)

    async def get_presigned_upload_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        return await self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in,
        )

    async def get_presigned_download_url(
        self, bucket: str, key: str, expires_in: int = 3600
    ) -> str:
        return await self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in,
        )

    async def file_exists(self, bucket: str, key: str) -> bool:
        try:
            await self.client.head_object(Bucket=bucket, Key=key)
            return True
        except Exception:
            return False
