import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class BookingModel(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    tracking_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    carrier: Mapped[str] = mapped_column(String(50), nullable=False)
    origin_address: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_address: Mapped[str] = mapped_column(String(255), nullable=False)
    weight_kg: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="confirmed")
    confirmed_by_user: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
