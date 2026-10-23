import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class RAGChunkModel(Base):
    __tablename__ = "rag_document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_title: Mapped[str] = mapped_column(String(255), nullable=False)
    carrier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[list]] = mapped_column(Vector(768), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
