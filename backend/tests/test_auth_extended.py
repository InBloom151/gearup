import pytest
from httpx import AsyncClient
from starlette import status
from jose import JWTError, jwt

from app.api.v1.schemas.token import AccessToken
from app.core.config import settings


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, user_data):
    r1 = await client.post("/api/v1/auth/register", json=user_data.model_dump())
    assert r1.status_code == status.HTTP_201_CREATED

    r2 = await client.post("/api/v1/auth/register", json=user_data.model_dump())
    assert r2.status_code == status.HTTP_400_BAD_REQUEST
    assert r2.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_register_invalid_payload(client: AsyncClient):
    invalid = {"email": "no-pass@example.com", "name": "NoPass", "role": "client"}
    r = await client.post("/api/v1/auth/register", json=invalid)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(err["loc"][-1] == "password" for err in r.json()["detail"])


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, user_data):
    r = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json()["detail"] == "Invalid credentials"

    await client.post("/api/v1/auth/register", json=user_data.model_dump())
    r2 = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": "wrongpass"},
    )
    assert r2.status_code == status.HTTP_401_UNAUTHORIZED
    assert r2.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient):
    r1 = await client.post("/api/v1/auth/login", json={"password": "whatever"})
    assert r1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    r2 = await client.post("/api/v1/auth/login", json={"email": "a@b.com"})
    assert r2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_refresh_missing_cookie(client: AsyncClient):
    r = await client.post("/api/v1/auth/refresh")
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json()["detail"] == "Missing refresh token"


@pytest.mark.asyncio
async def test_refresh_invalid_token(client: AsyncClient):
    client.cookies.set(
        name="refresh_token",
        value="not.a.jwt",
        domain="testserver",
        path="/api/v1/auth",
    )
    r = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": "not.a.jwt"},
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r.json()["detail"] == "Invalid refresh token"


@pytest.mark.asyncio
async def test_refresh_nonexistent_user(client: AsyncClient, user_data):
    fake_token = jwt.encode(
        {"sub": "noone@example.com", "type": "refresh"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    r = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": fake_token},
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_login_and_refresh_rotation(client: AsyncClient, create_user, user_data):
    await create_user(user_data)

    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    assert login_res.status_code == 200
    token1 = AccessToken(**login_res.json()).access_token
    cookie1 = login_res.cookies.get("refresh_token")
    assert cookie1

    refresh_res = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": cookie1},
    )
    assert refresh_res.status_code == 200
    token2 = refresh_res.json()["access_token"]
    cookie2 = refresh_res.cookies.get("refresh_token")

    assert token1 != token2
    assert cookie1 != cookie2
    from jose import jwt  # noqa
    payload = jwt.decode(token2, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["type"] == "access"
    assert payload["sub"] == user_data.email


@pytest.mark.asyncio
async def test_protected_endpoint_requires_token(client: AsyncClient):
    r = await client.get("/api/v1/nonexistent")
    assert r.status_code == 404