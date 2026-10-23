from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.eval.schemas import EvalRunRequest, EvalMetricsSummary
from app.api.v1.eval.services import EvalService

router = APIRouter(prefix="/eval", tags=["Evaluation Framework"])

@router.post("/run")
async def run_evaluation_suite(
    payload: EvalRunRequest,
    db: AsyncSession = Depends(get_db)
):
    """Trigger execution of the logistics evaluation benchmark suite."""
    return await EvalService.run_benchmark(db, payload)

@router.get("/metrics", response_model=EvalMetricsSummary)
async def get_evaluation_metrics(
    db: AsyncSession = Depends(get_db)
):
    """Retrieve aggregate evaluation metrics summary for dashboard rendering."""
    return await EvalService.get_metrics(db)
