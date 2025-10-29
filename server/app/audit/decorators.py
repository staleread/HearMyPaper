from functools import wraps
from typing import Callable, Awaitable, TypeVar, ParamSpec

from fastapi import Request
from app.shared.utils.db import SqlRunner
from app.auth.models import Subject
from . import service as audit_service

P = ParamSpec("P")
R = TypeVar("R")


def audit() -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator for FastAPI route handlers that logs all actions to the audit log.
    Captures the function name as action, wraps in try-except to determine success,
    and logs HTTPException details as reason.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            action = func.__name__
            db = kwargs.get("db")
            subject = kwargs.get("subject")
            request = kwargs.get("request")

            if not isinstance(db, SqlRunner):
                raise RuntimeError(
                    f"Function {func.__name__} must have 'db' parameter of type SqlRunner for audit"
                )

            user_id: int | None = None
            if isinstance(subject, Subject):
                user_id = subject.id

            ip_address: str | None = None
            if isinstance(request, Request):
                ip_address = (
                    request.headers.get("do-connecting-ip")
                    or request.headers.get("X-Real-IP")
                    or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
                    or (request.client.host if request.client else None)
                )

            success = True
            reason: str | None = None

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                reason = getattr(e, "detail", str(e))
                raise
            finally:
                audit_service.add_action_log(
                    action=action,
                    is_success=success,
                    reason=reason,
                    user_id=user_id,
                    ip_address=ip_address,
                    db=db,
                )

        return wrapper

    return decorator
