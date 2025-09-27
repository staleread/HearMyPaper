from fastapi import Header
from typing import Annotated
from collections.abc import Callable

from app.shared.models import UserInfo
from app.auth import service as auth_service
from app.auth.enums import ConfidentialityLevel, SubjectAction


def authorize_subject(
    *,
    subject_action: SubjectAction = SubjectAction.READ,
    confidentiality_level: ConfidentialityLevel = ConfidentialityLevel.UNCLASSIFIED,
    object_categories: set[str] = set(),
) -> Callable[[Annotated[str | None, Header()]], UserInfo]:
    if object_categories is None:
        object_categories = set()

    def get_user(authorization: Annotated[str | None, Header()] = None) -> UserInfo:
        return auth_service.authorize_subject(
            auth_header=authorization,
            subject_action=subject_action,
            confidentiality_level=confidentiality_level,
            object_categories=object_categories,
        )

    return get_user
