import base64
from fastapi import APIRouter, HTTPException, Path
from app.shared.dependencies.db import PostgresRunnerDep
from . import repository

router = APIRouter()


@router.get("/{pseudonym}/public-key")
async def get_user_public_key(
    db: PostgresRunnerDep,
    pseudonym: str = Path(..., description="The user's pseudonym"),
):
    """
    Returns the public key for a given user pseudonym.
    Used by other workloads for Sealed Box encryption.
    """
    public_key_bytes = repository.get_public_key_by_pseudonym(pseudonym, db=db)
    if not public_key_bytes:
        raise HTTPException(status_code=404, detail="User not found")

    public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")
    return {"pseudonym": pseudonym, "public_key": public_key_b64}
