from datetime import datetime
from httpx import AsyncClient
from uuid import UUID

from client_core.models import ProcessingTaskType, Conversion, ConversionStatus
from client_core.ports.outgoing.processing import ProcessingPort, ConversionRequestInfo
from shared_kernel.marshal import from_b64


class ProcessingPortAdapter(ProcessingPort):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def request_conversion(
        self, source_id: UUID, task_type: ProcessingTaskType
    ) -> ConversionRequestInfo:
        payload = {
            "source_id": str(source_id),
            "task_type": task_type,
        }
        response = await self.client.post("/conversions", json=payload)
        response.raise_for_status()
        data = response.json()

        return ConversionRequestInfo(
            conversion_id=UUID(data["conversion_id"]),
            sealing_key=from_b64(data["sealing_key_b64"]),
            upload_url=data["upload_url"],
        )

    async def commit_conversion(self, conversion_id: UUID) -> None:
        response = await self.client.post(f"/conversions/{conversion_id}/commit")
        response.raise_for_status()

    async def get_my_conversions(self) -> list[Conversion]:
        response = await self.client.get("/conversions")
        response.raise_for_status()
        data = response.json()
        return [
            Conversion(
                id=UUID(c["conversion_id"]),
                source_id=UUID(c["source_id"]),
                status=ConversionStatus(c["status"]),
                created_at=datetime.fromisoformat(c["created_at"]),
            )
            for c in data
        ]

    async def get_conversion_download_url(self, conversion_id: UUID) -> str:
        response = await self.client.get(f"/conversions/{conversion_id}/download-url")
        response.raise_for_status()
        return response.json()["download_url"]
