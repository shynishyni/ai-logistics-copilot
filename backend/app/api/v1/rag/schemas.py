from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

class DocumentIngest(BaseModel):
    document_title: str
    carrier: Optional[str] = None
    category: Optional[str] = None
    content: str

class RAGQuery(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=10)
    carrier_filter: Optional[str] = None

class RAGSearchResult(BaseModel):
    chunk_id: UUID
    document_title: str
    carrier: Optional[str] = None
    category: Optional[str] = None
    content: str
    similarity_score: float

    class Config:
        from_attributes = True
