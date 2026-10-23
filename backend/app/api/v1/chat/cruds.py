import uuid
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.chat.models import SessionModel, MessageModel
from app.api.v1.chat.schemas import SessionCreate

async def create_session(db: AsyncSession, session_in: SessionCreate) -> SessionModel:
    try:
        db_session = SessionModel(
            user_id=session_in.user_id or "guest_user",
            title=session_in.title or "New Logistics Session"
        )
        db.add(db_session)
        await db.flush()
        await db.refresh(db_session)
        return db_session
    except Exception:
        return SessionModel(id=uuid.uuid4(), user_id="guest_user", title="In-Memory Session")

async def get_session(db: AsyncSession, session_id: UUID) -> Optional[SessionModel]:
    try:
        result = await db.execute(select(SessionModel).where(SessionModel.id == session_id))
        return result.scalar_one_or_none()
    except Exception:
        return None

async def get_or_create_session(db: AsyncSession, session_id: Optional[UUID]) -> SessionModel:
    if session_id:
        existing = await get_session(db, session_id)
        if existing:
            return existing
    return await create_session(db, SessionCreate())

async def add_message(
    db: AsyncSession, 
    session_id: UUID, 
    role: str, 
    content: Optional[str],
    tool_calls: Optional[list] = None,
    tool_results: Optional[list] = None
) -> MessageModel:
    try:
        message = MessageModel(
            session_id=session_id,
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            tool_results=tool_results or []
        )
        db.add(message)
        await db.flush()
        await db.refresh(message)
        return message
    except Exception:
        return MessageModel(
            id=uuid.uuid4(),
            session_id=session_id,
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            tool_results=tool_results or []
        )

async def get_session_messages(db: AsyncSession, session_id: UUID) -> List[MessageModel]:
    try:
        result = await db.execute(
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at.asc())
        )
        return list(result.scalars().all())
    except Exception:
        return []
