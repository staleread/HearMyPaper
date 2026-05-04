from uuid import UUID
from fastapi import HTTPException
from hmp_core.storage import ObjectStorageClient, SqlRunner
from hmp_core.auth import IdentityContext
from .dto import SubmissionIntentRequest, SubmissionIntentResponse
from . import repository

async def create_submission_intent(
    identity: IdentityContext,
    payload: SubmissionIntentRequest,
    *,
    db: SqlRunner,
    storage: ObjectStorageClient
) -> SubmissionIntentResponse:
    """
    Orchestrates the submission intent using the Trusted Headers identity context.
    """
    # 1. Resolve User
    user_id = repository.get_user_id_by_pseudonym(identity.user_pseudonym, db=db)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Verify Project Assignment
    ps_id = repository.get_project_student_id(payload.project_id, user_id, db=db)
    if ps_id is None:
        raise HTTPException(status_code=403, detail="Student is not assigned to this project")

    # 3. Construct Storage Path
    storage_path = f"submissions/{identity.user_pseudonym}/project-{payload.project_id}/{payload.filename}"

    # 4. Generate Pre-signed URL (15-min expiry)
    bucket_name = "hmp-submissions"
    await storage.ensure_bucket(bucket_name)
    upload_url = await storage.get_presigned_upload_url(
        bucket=bucket_name,
        key=storage_path,
        expires_in=900
    )

    # 5. Record Intent in DB
    submission_uuid = repository.insert_pending_submission(
        ps_id, storage_path, payload.content_hash, db=db
    )

    return SubmissionIntentResponse(
        upload_url=upload_url,
        submission_uuid=submission_uuid
    )

async def commit_submission(
    submission_uuid: UUID,
    identity: IdentityContext,
    *,
    db: SqlRunner,
    storage: ObjectStorageClient
) -> None:
    """
    Finalizes the submission lifecycle:
    1. Verifies submission exists and belongs to the user.
    2. Verifies the file actually exists in object storage.
    3. Updates status to 'uploaded' and logs the success.
    """
    # 1. Retrieve Submission
    submission = repository.get_submission_by_uuid(submission_uuid, db=db)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # 2. Security Check: Only the owner can commit
    if submission["user_pseudonym"] != identity.user_pseudonym:
        raise HTTPException(status_code=403, detail="Unauthorized to commit this submission")
    
    if submission["status"] != 'pending':
        raise HTTPException(status_code=400, detail=f"Submission is already in {submission['status']} state")

    # 3. Storage Verification
    bucket_name = "hmp-submissions"
    if not await storage.file_exists(bucket_name, submission["storage_path"]):
        raise HTTPException(status_code=400, detail="File not found in storage. Please upload before committing.")

    # 4. Finalize
    # Resolve user_id for logging
    user_id = repository.get_user_id_by_pseudonym(identity.user_pseudonym, db=db)
    
    repository.update_submission_status(
        submission_uuid,
        status="uploaded",
        db=db,
        log_action="COMMIT_SUBMISSION",
        user_id=user_id,
        spiffe_id=identity.workload_id,
        pseudonym=identity.user_pseudonym,
        log_context={"storage_path": submission["storage_path"]}
    )
    
    # TODO: Future Event Dispatch (notify RabbitMQ for TTS if requested)
    print(f" [x] Submission {submission_uuid} committed and verified.")
