import pytest
from httpx import AsyncClient
from starlette import status

from app.api.v1.schemas.token import AccessToken


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient, user_data):
    # ------ register ------
    res = await client.post("/api/v1/auth/register", json=user_data.model_dump())
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["email"] == user_data.email

    # ------ login ------
    res = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    assert res.status_code == 200
    token = AccessToken(**res.json())
    assert token.token_type == "bearer"

    # refresh cookie должна появиться
    assert "refresh_token" in res.cookies

    # ------ access protected route (example) ------
    headers = {"Authorization": f"Bearer {token.access_token}"}
    protected = await client.get("/api/v1/health", headers=headers)
    assert protected.status_code == 200


@pytest.mark.asyncio
async def test_refresh_flow(client: AsyncClient, create_user, user_data):
    await create_user(user_data)

    # initial login
    res = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    refresh_cookie = res.cookies.get("refresh_token")
    access1 = res.json()["access_token"]

    # wait / simulate expire → call refresh
    res = await client.post("/api/v1/auth/refresh", cookies={"refresh_token": refresh_cookie})
    assert res.status_code == 200
    access2 = res.json()["access_token"]
    assert access1 != access2