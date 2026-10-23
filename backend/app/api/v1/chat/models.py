import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, default="guest_user")
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="New Logistics Session")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    messages: Mapped[List["MessageModel"]] = relationship("MessageModel", back_populates="session", cascade="all, delete-orphan")

class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False) # 'user', 'assistant', 'system', 'tool'
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tool_calls: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    tool_results: Mapped[Optional[dict]] = mapped_column(JSONB, default=list)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="messages")
