from functools import wraps
from typing import Callable, Awaitable, TypeVar, ParamSpec
from fastapi import HTTPException

from .models import ObjectId, Subject
from .enums import AccessType, AccessLevel
from .service import authorize_subject

P = ParamSpec("P")
R = TypeVar("R")


def authorize(
    access_level: AccessLevel,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator for FastAPI route handlers that enforces authorization.
    - Infers access_type from the CRU* function name.
    - Infers resource_type from the function name after the verb.
    - Extracts `id` (if present in path params) to build ObjectId.
    - Reads `subject`, which should be injected (e.g. as a FastAPI dependency)
    """

    access_map: dict[str, AccessType] = {
        "create": AccessType.WRITE,
        "read": AccessType.READ,
        "update": AccessType.READ | AccessType.WRITE,
    }

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            func_name = func.__name__
            try:
                verb, resource_type = func_name.split("_", 1)
            except ValueError:
                raise RuntimeError(
                    f"Function {func_name} must follow <verb>_<resource> naming convention"
                )

            if verb not in access_map:
                raise RuntimeError(
                    f"Unsupported verb '{verb}' in {func_name}. "
                    f"Use one of {list(access_map.keys())}"
                )

            access_type: AccessType = access_map[verb]

            subject = kwargs.get("subject")

            if not isinstance(subject, Subject):
                raise HTTPException(status_code=401, detail="Unauthorized")

            id_arg = kwargs.get("id")
            obj_id_val: int | None = id_arg if isinstance(id_arg, int) else None
            object_id = ObjectId(resource_type=resource_type, id=obj_id_val)

            authorize_subject(
                subject=subject,
                access_type=access_type,
                object_id=object_id,
                object_access_level=access_level,
            )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
