import asyncio
from asyncio import AbstractEventLoop

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from main import app
from src.database.connection import get_db
from src.settings import Settings


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def meta_migration():
    settings = Settings(ASYNC_MODE=False, TEST_MODE=True)
    sync_engine = create_engine(settings.postgres_url, echo=False)

    # SQLModel.metadata.drop_all(sync_engine)
    # SQLModel.metadata.create_all(sync_engine)

    yield sync_engine

    # SQLModel.metadata.drop_all(sync_engine)


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncEngine:
    settings = Settings(ASYNC_MODE=True, TEST_MODE=True)
    engine = create_async_engine(settings.postgres_url, echo=False)

    yield engine


@pytest_asyncio.fixture
async def session(async_engine):
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        async_session = AsyncSession(conn, expire_on_commit=False)

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session

        await async_session.close()
        await async_session.rollback()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_db]
