from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.rag.models import RAGChunkModel

async def add_chunk(
    db: AsyncSession,
    document_title: str,
    chunk_index: int,
    content: str,
    carrier: Optional[str] = None,
    category: Optional[str] = None,
    embedding: Optional[List[float]] = None
) -> RAGChunkModel:
    chunk = RAGChunkModel(
        document_title=document_title,
        chunk_index=chunk_index,
        content=content,
        carrier=carrier,
        category=category,
        embedding=embedding
    )
    db.add(chunk)
    await db.flush()
    await db.refresh(chunk)
    return chunk

async def search_similar_chunks(
    db: AsyncSession,
    query_vector: List[float],
    top_k: int = 3,
    carrier_filter: Optional[str] = None
) -> List[tuple[RAGChunkModel, float]]:
    # pgvector cosine distance: embedding.cosine_distance(query_vector)
    query = select(
        RAGChunkModel,
        RAGChunkModel.embedding.cosine_distance(query_vector).label("distance")
    )
    if carrier_filter:
        query = query.where(RAGChunkModel.carrier == carrier_filter)
    
    query = query.order_by("distance").limit(top_k)
    result = await db.execute(query)
    
    # Return (chunk, similarity_score)
    items = []
    for row in result.all():
        chunk, distance = row
        similarity = 1.0 - float(distance)
        items.append((chunk, similarity))
    return items
