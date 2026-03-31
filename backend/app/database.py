"""
Database connection and session management

Uses SQLModel (SQLAlchemy + Pydantic) for ORM.
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.config import settings


def get_async_database_url():
    """Convert DATABASE_URL to async-compatible format"""
    url = settings.DATABASE_URL
    # Handle different URL formats
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql+asyncpg://"):
        return url  # Already correct
    else:
        return url  # Return as-is for SQLite or other databases


def get_sync_database_url():
    """Convert DATABASE_URL to sync-compatible format"""
    url = settings.DATABASE_URL
    # Remove async prefixes for sync operations
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    elif url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql://", 1)
    elif url.startswith("postgresql://"):
        return url  # Already correct
    else:
        return url  # Return as-is for SQLite or other databases


# Create async engine
engine = create_async_engine(
    get_async_database_url(),
    echo=settings.is_development,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before use
)

# Create sync engine for migrations
sync_engine = create_engine(
    get_sync_database_url(),
    echo=settings.is_development,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync session factory (for migrations)
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        # Import all models to ensure they're registered with SQLModel
        from app.models import User, Module, Chapter, ChapterProgress, QuizAttempt, QuizQuestion, Achievement, UserAchievement, DailyStreak
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    
    Usage:
        @app.get("/items/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


def get_sync_db() -> Session:
    """
    Dependency for getting sync database session.
    Use for synchronous operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
