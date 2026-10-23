from pydantic import BaseModel, Field
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    session_id: Optional[UUID] = None
    content: str = Field(..., min_length=1, description="User message prompt")

class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = []
    tool_results: Optional[List[Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    user_id: Optional[str] = "guest_user"
    title: Optional[str] = "New Logistics Session"

class SessionResponse(BaseModel):
    id: UUID
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StreamChunk(BaseModel):
    event: str # 'delta', 'tool_call', 'tool_result', 'done', 'error'
    text: Optional[str] = None
    tool_data: Optional[Any] = None
