import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db import get_session
from app.models import Base


@pytest_asyncio.fixture(scope="session")
async def engine_and_connection():
    """
    Provides an async engine and a persistent connection.

    The in-memory SQLite database is created and kept open
    throughout the entire test session.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield engine, conn
    await engine.dispose()


@pytest_asyncio.fixture()
async def async_session(engine_and_connection):
    """
    Provides a new SQLAlchemy async session for each test.

    Uses the shared in-memory database connection.
    """
    engine, conn = engine_and_connection
    session_factory = sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture()
async def client(async_session):
    """
    Provides an HTTPX AsyncClient with the session overridden.

    This allows full-stack API testing with the database mocked
    through dependency injection.
    """
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session  # type: ignore

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()  # type: ignore
