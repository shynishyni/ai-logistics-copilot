from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.shipments import cruds
from app.api.v1.shipments.schemas import ShipmentRequest, CarrierQuote

class ShipmentService:
    @staticmethod
    async def get_state(db: AsyncSession, session_id: UUID):
        return await cruds.get_shipment_state(db, session_id)

    @staticmethod
    async def update_request(db: AsyncSession, session_id: UUID, req: ShipmentRequest):
        return await cruds.upsert_shipment_state(
            db,
            session_id=session_id,
            origin=req.origin.model_dump(),
            destination=req.destination.model_dump(),
            package_details={
                "weight": req.weight,
                "unit": req.weight_unit.value,
                "type": req.shipment_type.value
            },
            status="quoting"
        )
