from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.approval.schemas import ApprovalRequest
from app.api.v1.approval.services import ApprovalService

router = APIRouter(prefix="/approval", tags=["Human-in-the-Loop Approval"])

@router.post("/")
async def submit_approval_decision(
    payload: ApprovalRequest,
    db: AsyncSession = Depends(get_db)
):
    """Submit user authorization (Approve/Reject) for pending high-impact tool execution."""
    return await ApprovalService.process_approval(db, payload)
