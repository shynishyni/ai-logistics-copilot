from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.shipments.services import ShipmentService
from app.api.v1.shipments.schemas import ShipmentRequest

router = APIRouter(prefix="/shipments", tags=["Shipments"])

@router.get("/{session_id}")
async def get_shipment_workflow_state(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve active shipment workflow draft state for a session."""
    state = await ShipmentService.get_state(db, session_id)
    if not state:
        raise HTTPException(status_code=404, detail="No active shipment state found for this session")
    return state

@router.post("/{session_id}")
async def update_shipment_workflow_state(
    session_id: UUID,
    payload: ShipmentRequest,
    db: AsyncSession = Depends(get_db)
):
    """Update active shipment request parameters."""
    return await ShipmentService.update_request(db, session_id, payload)
