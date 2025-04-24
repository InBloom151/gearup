import pytest
from app.api.v1.schemas.landlord_detail import (
    LandlordDetailCreate,
    LandlordDetailUpdate,
)
from app.api.v1.schemas.user import UserCreate, UserUpdate
from app.core import security
from app.core.enums import EntityTypes
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_get_user_by_email_and_id(db_session, user_data):
    repo = UserRepository(db_session)
    dto = UserCreate(**user_data.model_dump())
    dto.password = security.hash_password(dto.password)
    user = await repo.create_user(dto)

    by_email = await repo.get_user_by_email(user.email)
    assert by_email and by_email.id == user.id

    by_id = await repo.get_user_by_id(user.id)
    assert by_id and by_id.email == user.email


@pytest.mark.asyncio
async def test_update_user(db_session, user_data):
    repo = UserRepository(db_session)
    dto = UserCreate(**user_data.model_dump())
    dto.password = security.hash_password(dto.password)
    user = await repo.create_user(dto)

    upd = UserUpdate(name="New Name", phone="123456")
    updated = await repo.update_user(user, upd)
    assert updated.name == "New Name"
    assert updated.phone == "123456"
    assert updated.email == user.email


@pytest.mark.asyncio
async def test_landlord_crud(db_session, user_data):
    repo = UserRepository(db_session)
    dto = UserCreate(**user_data.model_dump())
    dto.password = security.hash_password(dto.password)
    user = await repo.create_user(dto)

    assert await repo.get_landlord_by_user_id(user.id) is None

    ld_dto = LandlordDetailCreate(
        user_id=user.id,
        entity_type=EntityTypes.INDIVIDUAL,
    )
    ld = await repo.create_landlord(ld_dto)
    assert ld.user_id == user.id

    fetched = await repo.get_landlord_by_user_id(user.id)
    assert fetched and fetched.id == ld.id

    upd_ld = LandlordDetailUpdate(company_name="Comp")
    updated = await repo.update_landlord(ld, upd_ld)
    assert updated.company_name == "Comp"
