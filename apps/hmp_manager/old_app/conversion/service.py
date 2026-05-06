import uuid
from fastapi import HTTPException
from hmp_core.storage import ObjectStorageClient, SqlRunner
from hmp_core.auth import IdentityContext
from hmp_core.auth.utils import get_workload_claims
from hmp_core.events import ConversionJobTask, EventClient
from .dto import ConversionIntentRequest, ConversionIntentResponse
from . import repository
from app.user.repository import get_user_id_by_pseudonym


async def create_conversion_intent(
    identity: IdentityContext,
    payload: ConversionIntentRequest,
    *,
    db: SqlRunner,
    storage: ObjectStorageClient,
) -> ConversionIntentResponse:
    """
    Orchestrates the conversion intent for an Instructor:
    1. Resolves Instructor ID.
    2. Constructs processing path in MinIO.
    3. Generates a pre-signed URL for upload.
    4. Records the conversion job as 'queued'.
    """
    # 1. Resolve Instructor
    instructor_id = get_user_id_by_pseudonym(identity.user_pseudonym, db=db)
    if instructor_id is None:
        raise HTTPException(status_code=404, detail="Instructor not found")

    # 2. Construct Storage Path (Processing bucket)
    # The instructor uploads the re-encrypted file for the TTS worker
    # Path format: processing/instructor-{pseudonym}/sub-{id}/{filename}
    storage_path = f"processing/instructor-{identity.user_pseudonym}/sub-{payload.submission_id}/{payload.filename}"

    # 3. Generate Pre-signed URL
    bucket_name = "hmp-processing"
    await storage.ensure_bucket(bucket_name)
    upload_url = await storage.get_presigned_upload_url(
        bucket=bucket_name, key=storage_path, expires_in=900
    )

    # 4. Insert into database
    conversion_uuid = repository.insert_conversion_job(
        submission_id=payload.submission_id,
        instructor_id=instructor_id,
        input_path=storage_path,
        db=db,
    )

    return ConversionIntentResponse(
        upload_url=upload_url, conversion_uuid=conversion_uuid
    )


async def commit_conversion(
    conversion_uuid: uuid.UUID,
    identity: IdentityContext,
    *,
    db: SqlRunner,
    event_client: EventClient,
) -> None:
    """
    Finalizes the conversion intent:
    1. Verifies the job exists and is 'queued'.
    2. Verifies the instructor is the owner.
    3. Updates status to 'processing'.
    4. Dispatches ConversionJobTask to RabbitMQ.
    """
    # 1. Retrieve Job
    job = repository.get_conversion_by_uuid(conversion_uuid, db=db)
    if not job:
        raise HTTPException(status_code=404, detail="Conversion job not found")

    # 2. Security Check
    if job["instructor_pseudonym"] != identity.user_pseudonym:
        raise HTTPException(
            status_code=403, detail="Unauthorized to commit this conversion"
        )

    if job["status"] != "queued":
        raise HTTPException(
            status_code=400, detail=f"Job is already in {job['status']} state"
        )

    # 3. Update Status
    repository.update_conversion_status(conversion_uuid, status="processing", db=db)

    # 4. Dispatch Event
    # Resolve claims for the instructor to include in the task (for BLP checks in worker)
    claims = get_workload_claims(identity.workload_id)

    task = ConversionJobTask(
        job_id=conversion_uuid,
        subject_pseudonym=identity.user_pseudonym,
        # Instructor converts a student's lab for himself
        recipient_pseudonym=identity.user_pseudonym,
        confidentiality_level=claims.confidentiality_level,
        input_object_path=job["input_path"],
        correlation_id=str(uuid.uuid4()),
    )

    # Ensure exchange is declared before publishing
    await event_client.declare_exchange("hmp.jobs.tts")

    await event_client.publish(
        routing_key="job.request.pdf",
        payload=task.model_dump_json().encode(),
        correlation_id=task.correlation_id,
    )

    print(f" [x] Conversion {conversion_uuid} committed and dispatched.")
