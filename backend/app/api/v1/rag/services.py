from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from google import genai
from app.config import settings
from app.api.v1.rag import cruds
from app.api.v1.rag.schemas import DocumentIngest, RAGQuery, RAGSearchResult

class RAGService:
    @staticmethod
    def get_embedding(text: str) -> List[float]:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embedding.values

    @classmethod
    async def ingest_document(cls, db: AsyncSession, payload: DocumentIngest):
        # Chunk text into ~500 char blocks
        chunk_size = 500
        text = payload.content
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        ingested = []
        for idx, chunk_text in enumerate(chunks):
            embedding = cls.get_embedding(chunk_text) if settings.GEMINI_API_KEY else None
            chunk = await cruds.add_chunk(
                db,
                document_title=payload.document_title,
                chunk_index=idx,
                content=chunk_text,
                carrier=payload.carrier,
                category=payload.category,
                embedding=embedding
            )
            ingested.append(chunk)
        return {"document_title": payload.document_title, "chunks_ingested": len(ingested)}

    @classmethod
    async def query_knowledge(cls, db: AsyncSession, payload: RAGQuery) -> List[RAGSearchResult]:
        if not settings.GEMINI_API_KEY:
            return []
        query_vector = cls.get_embedding(payload.query)
        matches = await cruds.search_similar_chunks(
            db, 
            query_vector, 
            top_k=payload.top_k, 
            carrier_filter=payload.carrier_filter
        )
        results = []
        for chunk, score in matches:
            results.append(
                RAGSearchResult(
                    chunk_id=chunk.id,
                    document_title=chunk.document_title,
                    carrier=chunk.carrier,
                    category=chunk.category,
                    content=chunk.content,
                    similarity_score=score
                )
            )
        return results
