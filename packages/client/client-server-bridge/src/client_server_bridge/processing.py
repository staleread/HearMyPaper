from httpx import AsyncClient
from uuid import UUID

from client_core.models import ProcessingTaskType
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
