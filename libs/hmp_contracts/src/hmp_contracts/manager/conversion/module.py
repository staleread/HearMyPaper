from uuid import UUID

import httpx

from .dto import ConversionIntentRequest, ConversionIntentResponse


class ConversionModule:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def post_intent(
        self, req: ConversionIntentRequest
    ) -> ConversionIntentResponse:
        """Declares intent to convert a submission."""
        response = await self.client.post("/conversions/intent", json=req.model_dump())
        response.raise_for_status()
        return ConversionIntentResponse.model_validate(response.json())

    async def commit(self, conversion_uuid: UUID) -> None:
        """Finalizes a conversion job."""
        # Note the prefix /conversions matches hmp_manager/main.py include_router
        response = await self.client.post(f"/conversions/{conversion_uuid}/commit")
        response.raise_for_status()
