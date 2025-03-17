from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    participant_id: int

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    user1_id: int
    user2_id: int
    updated_at: datetime
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0

    class Config:
        orm_mode = True 