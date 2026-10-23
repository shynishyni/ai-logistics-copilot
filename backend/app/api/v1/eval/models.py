import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class EvalResultModel(Base):
    __tablename__ = "eval_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    test_case_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tool_selection_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    rag_faithfulness_score: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)
    structured_output_valid: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
