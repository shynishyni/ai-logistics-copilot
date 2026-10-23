from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.shipments.models import ShipmentStateModel

async def get_shipment_state(db: AsyncSession, session_id: UUID) -> Optional[ShipmentStateModel]:
    result = await db.execute(select(ShipmentStateModel).where(ShipmentStateModel.session_id == session_id))
    return result.scalar_one_or_none()

async def upsert_shipment_state(
    db: AsyncSession,
    session_id: UUID,
    origin: Optional[dict] = None,
    destination: Optional[dict] = None,
    package_details: Optional[dict] = None,
    selected_carrier: Optional[str] = None,
    quoted_rate: Optional[float] = None,
    status: Optional[str] = "draft"
) -> ShipmentStateModel:
    state = await get_shipment_state(db, session_id)
    if not state:
        state = ShipmentStateModel(session_id=session_id)
        db.add(state)

    if origin: state.origin = origin
    if destination: state.destination = destination
    if package_details: state.package_details = package_details
    if selected_carrier: state.selected_carrier = selected_carrier
    if quoted_rate is not None: state.quoted_rate = quoted_rate
    if status: state.status = status

    await db.flush()
    await db.refresh(state)
    return state
