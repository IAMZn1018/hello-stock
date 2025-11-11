from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatSessionBase(BaseModel):
    user_id: str

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    session_id: int
    role: str
    content: str
    image_path: Optional[str] = None

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatQuery(BaseModel):
    user_id: str
    query: str
    image_path: Optional[str] = None