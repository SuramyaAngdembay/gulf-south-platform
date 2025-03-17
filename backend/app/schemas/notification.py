from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    message: str
    data: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True 