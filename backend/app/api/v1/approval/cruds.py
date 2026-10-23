import random
import string
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.approval.models import BookingModel
from app.api.v1.approval.schemas import ApprovalRequest

def generate_tracking_number(carrier: str) -> str:
    prefix = carrier.upper()[:3]
    digits = ''.join(random.choices(string.digits, k=10))
    return f"{prefix}-{digits}"

async def create_booking(db: AsyncSession, req: ApprovalRequest) -> BookingModel:
    tracking = generate_tracking_number(req.carrier)
    booking = BookingModel(
        session_id=req.session_id,
        tracking_number=tracking,
        carrier=req.carrier,
        origin_address=req.origin,
        destination_address=req.destination,
        weight_kg=req.weight_kg,
        total_cost=req.estimated_cost,
        status="confirmed" if req.approved else "cancelled",
        confirmed_by_user=req.approved
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    return booking
