from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.chat.schemas import (
    MessageCreate, 
    MessageResponse, 
    SessionCreate, 
    SessionResponse
)
from app.api.v1.chat import cruds
from app.api.v1.chat.services import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat session."""
    return await cruds.create_session(db, session_in)

@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_chat_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Fetch session metadata by ID."""
    session = await cruds.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@router.get("/session/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Fetch message history for a chat session."""
    return await cruds.get_session_messages(db, session_id)

@router.post("/", response_model=MessageResponse)
async def send_chat_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """Send a message and get a full response (Non-streaming)."""
    session = await cruds.get_or_create_session(db, payload.session_id)
    
    # Save user message
    await cruds.add_message(db, session.id, role="user", content=payload.content)
    
    # Process through ChatService
    assistant_text = await ChatService.process_chat(db, session.id, payload.content)
    
    # Retrieve saved assistant message
    messages = await cruds.get_session_messages(db, session.id)
    return messages[-1]

@router.post("/stream")
async def send_chat_message_stream(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """Send a message and stream response tokens via Server-Sent Events (SSE)."""
    session = await cruds.get_or_create_session(db, payload.session_id)
    
    return StreamingResponse(
        ChatService.stream_chat(db, session.id, payload.content),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
