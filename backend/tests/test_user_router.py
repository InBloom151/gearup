import pytest
from starlette import status


@pytest.mark.asyncio
async def test_update_user_router(client, create_user, user_data):
    await create_user(user_data)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.put(
        "/api/v1/user/update_user",
        json={"name": "RouterTest"},
        headers=headers,
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["name"] == "RouterTest"


@pytest.mark.asyncio
async def test_create_and_update_landlord_router(client, create_user, user_data):
    await create_user(user_data)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": user_data.email, "password": user_data.password},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res1 = await client.put(
        "/api/v1/user/update_landlord_detail",
        json={"company_name": "Nope"},
        headers=headers,
    )
    assert res1.status_code == status.HTTP_404_NOT_FOUND

    data = {"entity_type": "individual", "company_name": "Comp"}
    res2 = await client.post(
        "/api/v1/user/create_landlord_detail",
        json=data,
        headers=headers,
    )
    assert res2.status_code == status.HTTP_200_OK
    body = res2.json()
    assert body["entity_type"] == "individual"
    assert body["user"]["email"] == user_data.email

    res3 = await client.post(
        "/api/v1/user/create_landlord_detail", json=data, headers=headers
    )
    assert res3.status_code == status.HTTP_400_BAD_REQUEST

    res4 = await client.put(
        "/api/v1/user/update_landlord_detail",
        json={"company_name": "NewComp"},
        headers=headers,
    )
    assert res4.status_code == status.HTTP_200_OK
    assert res4.json()["company_name"] == "NewComp"
