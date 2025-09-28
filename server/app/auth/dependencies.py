from fastapi import Header, HTTPException, Depends
from typing import Annotated

from app.auth.models import Subject
from app.auth.utils import decode_subject_token


def get_current_subject(
    authorization: Annotated[str | None, Header()] = None,
) -> Subject:
    """
    Extract and validate the current subject from the Authorization header.

    Expected format: "Bearer <token>"
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=400,
            detail="Invalid Authorization header format",
        )

    token = parts[1]
    subject = decode_subject_token(token)

    if not subject:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    return subject


CurrentSubjectDep = Annotated[Subject, Depends(get_current_subject)]
