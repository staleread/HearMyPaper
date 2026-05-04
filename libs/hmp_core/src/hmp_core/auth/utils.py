from typing import Any

from fastapi import Request
from fastapi.exceptions import HTTPException

from .enums import AccessLevel, AccessType
from .models import AccessClaims

# Static workload registry for development/testing
STATIC_WORKLOAD_CLAIMS: dict[str, AccessClaims] = {
    "spiffe://hmp.internal/converter": AccessClaims(
        confidentiality_level=AccessLevel.RESTRICTED,
        integrity_levels=[AccessLevel.RESTRICTED],
    ),
    "spiffe://hmp.internal/manager": AccessClaims(
        confidentiality_level=AccessLevel.CONFIDENTIAL,
        integrity_levels=[
            AccessLevel.UNCLASSIFIED,
            AccessLevel.CONTROLLED,
            AccessLevel.RESTRICTED,
            AccessLevel.CONFIDENTIAL,
        ],
    ),
}


def get_workload_claims(spiffe_id: str | None) -> AccessClaims:
    """Retrieve subject claims from the static registry."""
    if not spiffe_id:
        return AccessClaims(
            confidentiality_level=AccessLevel.UNCLASSIFIED,
            integrity_levels=[AccessLevel.UNCLASSIFIED],
        )

    return STATIC_WORKLOAD_CLAIMS.get(
        spiffe_id,
        AccessClaims(
            confidentiality_level=AccessLevel.UNCLASSIFIED,
            integrity_levels=[AccessLevel.UNCLASSIFIED],
        ),
    )


async def resolve_workload_access_claims(kwargs: dict[str, Any]) -> AccessClaims:
    """
    Extract the workload identity (SPIFFE) and resolve its claims.
    Priority: OPA (future) -> Static Registry.
    """
    request = kwargs.get("request")
    if not isinstance(request, Request):
        raise RuntimeError(
            "FastAPI Request object missing in function arguments. "
            "Ensure 'request: Request' is in the route signature."
        )

    spiffe_id = getattr(request.state, "spiffe_id", None)

    # In production, we'd use the OPAClient here:
    # claims = await OPAClient().get_workload_claims(spiffe_id)
    # if claims: return claims

    return get_workload_claims(spiffe_id)


def resolve_user_access_claims(kwargs: dict[str, Any]) -> AccessClaims:
    """Extract and validate the user access claims from the injected dependencies."""
    user_access_claims = kwargs.get("subject")

    if not isinstance(user_access_claims, AccessClaims):
        raise HTTPException(status_code=401, detail="User unauthorized")

    return user_access_claims


def resolve_access_type(func_name: str) -> AccessType:
    """Resolve AccessType from function name (verb_resource)."""
    try:
        verb, _ = func_name.split("_", 1)
    except ValueError:
        raise RuntimeError(
            f"Function {func_name} must follow <verb>_<resource> naming convention"
        ) from None

    match verb:
        case "create" | "delete":
            return AccessType.WRITE
        case "read":
            return AccessType.READ
        case "update" | "execute":
            return AccessType.READ | AccessType.WRITE
        case _:
            supported = ["create", "read", "update", "execute", "delete"]
            raise RuntimeError(
                f"Unsupported verb '{verb}' in {func_name}. Use one of {supported}"
            )


def authorize_subject(
    subject: AccessClaims,
    *,
    access_type: AccessType,
    object_access_level: AccessLevel,
    identity_label: str = "Subject",
) -> None:
    """Authorize a single subject using Bell–LaPadula rules."""
    if (
        AccessType.READ in access_type
        and subject.confidentiality_level < object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"{identity_label} read access forbidden: confidentiality level "
                f"{subject.confidentiality_level.name} < object level "
                f"{object_access_level.name}"
            ),
        )

    if (
        AccessType.WRITE in access_type
        and subject.confidentiality_level > object_access_level
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"{identity_label} write access forbidden (no write down): "
                f"confidentiality level {subject.confidentiality_level.name} "
                f"> object level {object_access_level.name}"
            ),
        )

    if (
        AccessType.WRITE in access_type
        and object_access_level not in subject.integrity_levels
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"{identity_label} write access forbidden: not authorized to write at "
                f"{object_access_level.name} level"
            ),
        )


def authorize_composite_identity(
    *,
    workload_claims: AccessClaims,
    user_claims: AccessClaims,
    access_type: AccessType,
    object_access_level: AccessLevel,
) -> None:
    """Enforce Stacked Authorization for both workload and user."""
    authorize_subject(
        user_claims,
        access_type=access_type,
        object_access_level=object_access_level,
        identity_label="User",
    )
    authorize_subject(
        workload_claims,
        access_type=access_type,
        object_access_level=object_access_level,
        identity_label="Workload",
    )
