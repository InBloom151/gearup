from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.db.base import Base
from app.db.session import get_session
from app import create_app

# ───────── in‑memory DB & session override ──────────────────────
@pytest_asyncio.fixture(scope="session")
async def _engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

# ───────── FastAPI test‑client ──────────────────────────────────
@asynccontextmanager
async def _lifespan(_: FastAPI):
    yield

@pytest_asyncio.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    app = create_app(lifespan=_lifespan)
    app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac