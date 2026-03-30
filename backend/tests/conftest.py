"""
Conftest - Pytest fixtures and configuration

Shared fixtures for all tests.
"""

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from jose import jwt

from app.main import app
from app.database import get_db
from app.models.user import User, Subscription
from app.models.chapter import Module, Chapter
from app.models.progress import ChapterProgress, QuizQuestion, QuizAttempt
from app.models.achievement import Achievement, UserAchievement, DailyStreak
from app.config import settings


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio backend for async tests"""
    return "asyncio"


@pytest.fixture(scope="function")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,  # Don't log SQL for cleaner output
        poolclass=StaticPool,  # Required for SQLite in-memory
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Module.metadata.create_all)
        await conn.run_sync(Chapter.metadata.create_all)
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Subscription.metadata.create_all)
        await conn.run_sync(ChapterProgress.metadata.create_all)
        await conn.run_sync(QuizQuestion.metadata.create_all)
        await conn.run_sync(QuizAttempt.metadata.create_all)
        await conn.run_sync(Achievement.metadata.create_all)
        await conn.run_sync(UserAchievement.metadata.create_all)
        await conn.run_sync(DailyStreak.metadata.create_all)
    
    yield engine
    
    # Cleanup
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()  # Rollback after each test


@pytest.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client"""
    
    # Override dependency
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Use httpx AsyncClient with ASGI transport
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def sample_user(test_db: AsyncSession) -> User:
    """Create sample user"""
    user = User(
        email="test@example.com",
        full_name="Test User"
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def sample_module(test_db: AsyncSession) -> Module:
    """Create sample module"""
    module = Module(
        title="Introduction to Generative AI",
        description="Learn the basics of generative AI",
        module_order=1
    )
    test_db.add(module)
    await test_db.commit()
    await test_db.refresh(module)
    return module


@pytest.fixture
async def sample_chapter(test_db: AsyncSession, sample_module: Module) -> Chapter:
    """Create sample chapter"""
    chapter = Chapter(
        chapter_number=1,
        module_id=sample_module.id,
        title="What is Generative AI?",
        content="# What is Generative AI?\n\nGenerative AI refers to...",
        is_free=True,
        estimated_minutes=15,
        order_in_module=1
    )
    test_db.add(chapter)
    await test_db.commit()
    await test_db.refresh(chapter)
    return chapter


@pytest.fixture
async def sample_quiz_question(test_db: AsyncSession, sample_chapter: Chapter) -> QuizQuestion:
    """Create sample quiz question"""
    question = QuizQuestion(
        chapter_id=sample_chapter.id,
        question_text="What does AI stand for?",
        options_json='{"A": "Artificial Intelligence", "B": "Automated Information", "C": "Advanced Interface", "D": "Algorithmic Integration"}',
        correct_answer="A",
        explanation="AI stands for Artificial Intelligence.",
        order_in_chapter=1
    )
    test_db.add(question)
    await test_db.commit()
    await test_db.refresh(question)
    return question


@pytest.fixture
async def sample_premium_user(test_db: AsyncSession) -> User:
    """Create sample premium user"""
    user = User(
        email="premium@example.com",
        full_name="Premium User"
    )
    test_db.add(user)
    
    subscription = Subscription(
        user_id=user.id,
        tier="premium",
        status="active"
    )
    test_db.add(subscription)
    
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def valid_token(sample_user: User) -> str:
    """Create valid JWT token for testing"""
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "user_id": sample_user.id,
        "email": sample_user.email,
        "exp": expire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.fixture
def premium_token(sample_premium_user: User) -> str:
    """Create valid JWT token for premium user"""
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "user_id": sample_premium_user.id,
        "email": sample_premium_user.email,
        "exp": expire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.fixture
def auth_headers(valid_token: str) -> dict:
    """Create authorization headers"""
    return {"Authorization": f"Bearer {valid_token}"}


@pytest.fixture
def premium_auth_headers(premium_token: str) -> dict:
    """Create authorization headers for premium user"""
    return {"Authorization": f"Bearer {premium_token}"}
