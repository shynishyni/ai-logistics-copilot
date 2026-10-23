import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.eval import cruds
from app.api.v1.eval.schemas import EvalRunRequest

class EvalService:
    @staticmethod
    async def run_benchmark(db: AsyncSession, req: EvalRunRequest):
        run_id = uuid.uuid4()
        
        # Sample benchmark run generator
        for idx in range(req.num_samples):
            await cruds.add_eval_result(
                db,
                run_id=run_id,
                test_case_name=f"test_case_{idx+1}",
                tool_correct=True,
                rag_score=0.95,
                struct_valid=True,
                latency_ms=450 + (idx * 20),
                total_tokens=320,
                passed=True
            )
        
        return {
            "run_id": str(run_id),
            "status": "completed",
            "samples_evaluated": req.num_samples
        }

    @staticmethod
    async def get_metrics(db: AsyncSession):
        return await cruds.get_latest_metrics(db)
