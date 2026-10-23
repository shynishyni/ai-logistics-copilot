from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import engine, Base
from app.api.v1.chat.routers import router as chat_router
from app.api.v1.shipments.routers import router as shipments_router
from app.api.v1.approval.routers import router as approval_router
from app.api.v1.rag.routers import router as rag_router
from app.api.v1.eval.routers import router as eval_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            # Enable pgvector extension first
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            await conn.run_sync(Base.metadata.create_all)
        print("[DB] PostgreSQL database connected & tables initialized successfully.")
    except Exception as e:
        print(f"[DB Notice] Could not initialize PostgreSQL: {e}")
        print("[DB Notice] Operating with in-memory fallback. Server is active.")
    yield
    # Cleanup connection engine on shutdown
    try:
        await engine.dispose()
    except Exception:
        pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise AI Logistics Copilot Backend Engine",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular feature domain routers
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(shipments_router, prefix=settings.API_V1_STR)
app.include_router(approval_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(eval_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }
