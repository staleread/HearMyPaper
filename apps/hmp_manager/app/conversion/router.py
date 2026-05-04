from uuid import UUID
from fastapi import APIRouter, Depends, status
from hmp_core.auth import IdentityDep
from app.shared.dependencies.db import PostgresRunnerDep
from app.shared.dependencies.storage import get_storage_client, ObjectStorageClient
from app.shared.dependencies.rabbitmq import get_event_client
from hmp_core.events import EventClient
from .dto import ConversionIntentRequest, ConversionIntentResponse
from . import service

router = APIRouter()

@router.post("/intent", response_model=ConversionIntentResponse)
async def post_conversion_intent(
    payload: ConversionIntentRequest,
    identity: IdentityDep,
    db: PostgresRunnerDep,
    storage: ObjectStorageClient = Depends(get_storage_client)
):
    """
    Endpoint for instructors to declare intent to convert a submission.
    Returns a pre-signed URL for upload to the processing bucket.
    """
    return await service.create_conversion_intent(
        identity, payload, db=db, storage=storage
    )

@router.post("/{conversion_uuid}/commit", status_code=status.HTTP_204_NO_CONTENT)
async def post_conversion_commit(
    conversion_uuid: UUID,
    identity: IdentityDep,
    db: PostgresRunnerDep,
    event_client: EventClient = Depends(get_event_client)
):
    """
    Finalizes a conversion job after the client has uploaded the re-encrypted file.
    Updates the status and dispatches the task to the TTS worker.
    """
    await service.commit_conversion(
        conversion_uuid, identity, db=db, event_client=event_client
    )
