from typing import Optional
from pydantic import BaseModel


class ActionLogResponse(BaseModel):
    timestamp: str
    action: str
    is_success: bool
    reason: Optional[str] = None
    user_name: Optional[str] = None
    ip_address: Optional[str] = None
