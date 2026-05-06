from uuid import UUID
from fastapi import APIRouter, Depends, status
from hmp_core.auth import IdentityDep
from app.shared.dependencies.db import PostgresRunnerDep
from app.shared.dependencies.storage import get_storage_client, ObjectStorageClient
from .dto import SubmissionIntentRequest, SubmissionIntentResponse
from . import service

router = APIRouter()


@router.post("/intent", response_model=SubmissionIntentResponse)
async def post_submission_intent(
    payload: SubmissionIntentRequest,
    identity: IdentityDep,
    db: PostgresRunnerDep,
    storage: ObjectStorageClient = Depends(get_storage_client),
):
    """
    Endpoint for students to declare their intent to submit an encrypted PDF.
    Returns a pre-signed URL for direct upload to MinIO.
    """
    return await service.create_submission_intent(
        identity, payload, db=db, storage=storage
    )


@router.post("/{submission_uuid}/commit", status_code=status.HTTP_204_NO_CONTENT)
async def post_submission_commit(
    submission_uuid: UUID,
    identity: IdentityDep,
    db: PostgresRunnerDep,
    storage: ObjectStorageClient = Depends(get_storage_client),
):
    """
    Finalizes a submission after the client has uploaded the file to MinIO.
    Verifies file existence and updates the submission status.
    """
    await service.commit_submission(submission_uuid, identity, db=db, storage=storage)
