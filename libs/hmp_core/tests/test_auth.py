import pytest
from fastapi.exceptions import HTTPException

from hmp_core.auth.enums import AccessLevel, AccessType
from hmp_core.auth.models import AccessClaims
from hmp_core.auth.utils import (
    authorize_composite_identity,
    get_workload_claims,
)


def test_authorize_composite_identity_success():
    user = AccessClaims(
        confidentiality_level=AccessLevel.RESTRICTED,
        integrity_levels=[AccessLevel.RESTRICTED],
    )
    workload = AccessClaims(
        confidentiality_level=AccessLevel.RESTRICTED,
        integrity_levels=[AccessLevel.RESTRICTED],
    )

    # Both have RESTRICTED, reading RESTRICTED should succeed
    authorize_composite_identity(
        workload_claims=workload,
        user_claims=user,
        access_type=AccessType.READ,
        object_access_level=AccessLevel.RESTRICTED,
    )


def test_authorize_composite_identity_user_fail():
    user = AccessClaims(
        confidentiality_level=AccessLevel.CONTROLLED,  # Lower than RESTRICTED
        integrity_levels=[AccessLevel.CONTROLLED],
    )
    workload = AccessClaims(
        confidentiality_level=AccessLevel.RESTRICTED,
        integrity_levels=[AccessLevel.RESTRICTED],
    )

    with pytest.raises(HTTPException) as exc:
        authorize_composite_identity(
            workload_claims=workload,
            user_claims=user,
            access_type=AccessType.READ,
            object_access_level=AccessLevel.RESTRICTED,
        )
    assert exc.value.status_code == 403
    assert "User read access forbidden" in exc.value.detail


def test_authorize_composite_identity_workload_fail():
    user = AccessClaims(
        confidentiality_level=AccessLevel.RESTRICTED,
        integrity_levels=[AccessLevel.RESTRICTED],
    )
    workload = AccessClaims(
        confidentiality_level=AccessLevel.CONTROLLED,  # Lower than RESTRICTED
        integrity_levels=[AccessLevel.CONTROLLED],
    )

    with pytest.raises(HTTPException) as exc:
        authorize_composite_identity(
            workload_claims=workload,
            user_claims=user,
            access_type=AccessType.READ,
            object_access_level=AccessLevel.RESTRICTED,
        )
    assert exc.value.status_code == 403
    assert "Workload read access forbidden" in exc.value.detail


def test_get_workload_claims_default():
    claims = get_workload_claims(None)
    assert claims.confidentiality_level == AccessLevel.UNCLASSIFIED


def test_get_workload_claims_known():
    claims = get_workload_claims("spiffe://hmp.internal/converter")
    assert claims.confidentiality_level == AccessLevel.RESTRICTED
