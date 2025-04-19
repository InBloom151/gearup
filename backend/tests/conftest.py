import os
import pytest
import pytest_asyncio

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app import create_app
from app.core.config import settings
from app.db.base import Base
from app.db.models import User, LandlordDetail

from app.db.session import get_session
from app.repositories.user import UserRepository
from app.api.v1.schemas.user import UserCreate
from app.core import security

# ────────────────── pick up test .env ───────────────────
os.environ.setdefault("APP_ENV", "test")

# ───────── pytest plugins for asyncio ───────────────
@pytest.fixture(autouse=True)
def _pytest_asyncio_config():
    return {"asyncio_mode": "auto"}


# ───────── in‑memory DB & session ──────────────────────
@pytest_asyncio.fixture(scope="session")
async def _engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        # cleanup: delete all rows so next test starts with an empty database
        await session.execute(delete(LandlordDetail))
        await session.execute(delete(User))
        await session.commit()


# ───────── user_data & create_user ────────────────────
@pytest.fixture
def user_data() -> UserCreate:
    """Default user payload for tests."""
    return UserCreate(
        email="user@example.com",
        password="secret123",
        name="Test User",
        role="client",
    )

@pytest_asyncio.fixture
async def create_user(db_session: AsyncSession) -> Callable[[UserCreate], None]:
    """
    Создаёт нового пользователя в БД, НЕ мутируя оригинальный user_data.
    """
    async def _factory(data: UserCreate) -> None:
        dto = UserCreate(**data.model_dump())
        dto.password = security.hash_password(dto.password)
        await UserRepository(db_session).create(dto)
    return _factory


# ───────── FastAPI test‑client ───────────────────────
@asynccontextmanager
async def _lifespan(_: FastAPI):
    yield  # skip startup/shutdown logic in tests

@pytest_asyncio.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    app = create_app(lifespan=_lifespan)
    # override the DB dependency
    app.dependency_overrides[get_session] = lambda: db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac