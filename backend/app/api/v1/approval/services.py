from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.approval import cruds
from app.api.v1.approval.schemas import ApprovalRequest

class ApprovalService:
    @staticmethod
    async def process_approval(db: AsyncSession, req: ApprovalRequest):
        if not req.approved:
            return {"status": "rejected", "message": "Booking was cancelled by the user."}
        
        booking = await cruds.create_booking(db, req)
        return {
            "status": "confirmed",
            "booking_id": booking.id,
            "tracking_number": booking.tracking_number,
            "carrier": booking.carrier,
            "total_cost": float(booking.total_cost)
        }
