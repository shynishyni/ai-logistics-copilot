from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ApprovalRequest(BaseModel):
    session_id: UUID
    approved: bool
    carrier: str
    origin: str
    destination: str
    weight_kg: float
    estimated_cost: float

class BookingResponse(BaseModel):
    booking_id: UUID
    tracking_number: str
    status: str
    carrier: str
    total_cost: float

    class Config:
        from_attributes = True
