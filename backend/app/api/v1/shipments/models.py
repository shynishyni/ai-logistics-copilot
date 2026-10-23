import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

class ShipmentStateModel(Base):
    __tablename__ = "shipment_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    origin: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    destination: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    package_details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    selected_carrier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quoted_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
