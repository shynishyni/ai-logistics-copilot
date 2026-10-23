from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class TestCase(BaseModel):
    name: str
    user_query: str
    expected_tool: Optional[str] = None
    expected_carrier: Optional[str] = None

class EvalRunRequest(BaseModel):
    run_name: Optional[str] = "Benchmark Suite 100"
    num_samples: int = 10

class EvalMetricsSummary(BaseModel):
    total_tests: int
    passed_tests: int
    tool_accuracy_percent: float
    rag_faithfulness_percent: float
    avg_latency_ms: float
    avg_tokens_per_call: float
