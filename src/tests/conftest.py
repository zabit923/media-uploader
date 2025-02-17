import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import app
from core.database import get_async_session, get_test_async_session, test_engine
from core.database.models import Base, User


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_session(init_db) -> AsyncSession:
    async for session in get_test_async_session():
        await session.execute(delete(User))
        await session.commit()
        yield session
        await session.close()


@pytest_asyncio.fixture
async def client(init_db) -> AsyncClient:
    async def override_get_test_session():
        async for session in get_test_async_session():
            yield session

    app.dependency_overrides[get_async_session] = override_get_test_session

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app), base_url="http://test"
        ) as async_client:
            yield async_client
