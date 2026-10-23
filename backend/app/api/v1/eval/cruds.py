from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.api.v1.eval.models import EvalResultModel
from app.api.v1.eval.schemas import EvalMetricsSummary

async def add_eval_result(
    db: AsyncSession,
    run_id: UUID,
    test_case_name: str,
    tool_correct: bool,
    rag_score: float,
    struct_valid: bool,
    latency_ms: int,
    total_tokens: int,
    passed: bool
) -> EvalResultModel:
    result = EvalResultModel(
        run_id=run_id,
        test_case_name=test_case_name,
        tool_selection_correct=tool_correct,
        rag_faithfulness_score=rag_score,
        structured_output_valid=struct_valid,
        latency_ms=latency_ms,
        total_tokens=total_tokens,
        passed=passed
    )
    db.add(result)
    await db.flush()
    await db.refresh(result)
    return result

async def get_latest_metrics(db: AsyncSession) -> EvalMetricsSummary:
    result = await db.execute(
        select(
            func.count(EvalResultModel.id).label("total"),
            func.sum(func.cast(EvalResultModel.passed, Integer)).label("passed_cnt"),
            func.avg(func.cast(EvalResultModel.tool_selection_correct, Integer)).label("tool_acc"),
            func.avg(EvalResultModel.rag_faithfulness_score).label("rag_score"),
            func.avg(EvalResultModel.latency_ms).label("avg_lat"),
            func.avg(EvalResultModel.total_tokens).label("avg_tok")
        )
    )
    row = result.first()
    total = row.total or 0
    passed = row.passed_cnt or 0
    tool_acc = (row.tool_acc or 0.0) * 100
    rag_score = (row.rag_score or 0.0) * 100
    avg_lat = float(row.avg_lat or 0.0)
    avg_tok = float(row.avg_tok or 0.0)

    return EvalMetricsSummary(
        total_tests=total,
        passed_tests=passed,
        tool_accuracy_percent=tool_acc,
        rag_faithfulness_percent=rag_score,
        avg_latency_ms=avg_lat,
        avg_tokens_per_call=avg_tok
    )
