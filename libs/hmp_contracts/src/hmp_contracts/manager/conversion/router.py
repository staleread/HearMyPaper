from uuid import UUID

import httpx

from .dto import ConversionIntentRequest, ConversionIntentResponse


async def post_conversion_intent(
    client: httpx.AsyncClient, base_url: str, req: ConversionIntentRequest
) -> ConversionIntentResponse:
    """Declares intent to convert a submission."""
    response = await client.post(
        f"{base_url}/conversions/intent", json=req.model_dump()
    )
    response.raise_for_status()
    return ConversionIntentResponse.model_validate(response.json())


async def commit_conversion(
    client: httpx.AsyncClient, base_url: str, conversion_uuid: UUID
) -> None:
    """Finalizes a conversion job."""
    response = await client.post(f"{base_url}/conversions/{conversion_uuid}/commit")
    response.raise_for_status()
