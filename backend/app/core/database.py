from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

# Create async engine with pooled connections
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.LOG_LEVEL == "DEBUG"),
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    except Exception:
        # DB offline fallback for development without active PostgreSQL service
        yield None
