from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.rag.schemas import DocumentIngest, RAGQuery, RAGSearchResult
from app.api.v1.rag.services import RAGService

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Engine"])

@router.post("/ingest")
async def ingest_logistics_document(
    payload: DocumentIngest,
    db: AsyncSession = Depends(get_db)
):
    """Ingest logistics document PDF/text into pgvector database."""
    return await RAGService.ingest_document(db, payload)

@router.post("/query", response_model=List[RAGSearchResult])
async def search_logistics_knowledge(
    payload: RAGQuery,
    db: AsyncSession = Depends(get_db)
):
    """Perform hybrid similarity vector search using pgvector."""
    return await RAGService.query_knowledge(db, payload)
