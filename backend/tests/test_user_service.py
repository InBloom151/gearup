import pytest
from app.api.v1.schemas.landlord_detail import (
    LandlordDetailCreate,
    LandlordDetailUpdate,
)
from app.api.v1.schemas.user import UserCreate, UserUpdate
from app.core import security
from app.core.enums import EntityTypes
from app.repositories.user import UserRepository
from app.services.user import UserService
from fastapi import HTTPException
from starlette import status


@pytest.mark.asyncio
async def test_update_nonexistent_user(db_session):
    svc = UserService(db_session)
    with pytest.raises(HTTPException) as exc:
        await svc.update_user(UserUpdate(name="X"), 999)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user_success(db_session, user_data):
    dto = UserCreate(**user_data.model_dump())
    dto.password = security.hash_password(dto.password)
    repo = UserRepository(db_session)
    user = await repo.create_user(dto)

    svc = UserService(db_session)
    res = await svc.update_user(UserUpdate(name="OK"), user.id)
    assert res.id == user.id
    assert res.name == "OK"


@pytest.mark.asyncio
async def test_create_landlord_detail_and_duplicate(db_session, user_data):
    dto = UserCreate(**user_data.model_dump())
    dto.password = security.hash_password(dto.password)
    repo = UserRepository(db_session)
    user = await repo.create_user(dto)

    svc = UserService(db_session)
    ld_data = LandlordDetailCreate(
        user_id=user.id,
        entity_type=EntityTypes.INDIVIDUAL,
    )
    ld = await svc.create_landlord_detail(ld_data)
    assert ld.user_id == user.id

    with pytest.raises(HTTPException) as exc:
        await svc.create_landlord_detail(ld_data)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_landlord_detail_errors_and_success(db_session, user_data):
    svc = UserService(db_session)
    with pytest.raises(HTTPException) as exc1:
        await svc.update_landlord_detail(LandlordDetailUpdate(company_name="X"), 1)
    assert exc1.value.status_code == status.HTTP_404_NOT_FOUND

    repo = UserRepository(db_session)
    d1 = UserCreate(**user_data.model_dump())
    d1.password = security.hash_password(d1.password)
    u1 = await repo.create_user(d1)
    d2 = UserCreate(
        email="other@example.com",
        password="pass1234",
        name="Other",
        role=user_data.role,
    )
    d2.password = security.hash_password(d2.password)
    u2 = await repo.create_user(d2)

    await repo.create_landlord(
        LandlordDetailCreate(user_id=u1.id, entity_type=EntityTypes.LEGAL)
    )
    with pytest.raises(HTTPException):
        await svc.update_landlord_detail(LandlordDetailUpdate(company_name="X"), u2.id)

    res = await svc.update_landlord_detail(
        LandlordDetailUpdate(company_name="OK"), u1.id
    )
    assert res.company_name == "OK"
