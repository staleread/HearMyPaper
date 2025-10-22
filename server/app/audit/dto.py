from pydantic import BaseModel


class ActionLogResponse(BaseModel):
    timestamp: str
    action: str
    is_success: bool
    reason: str | None
    user_name: str | None
