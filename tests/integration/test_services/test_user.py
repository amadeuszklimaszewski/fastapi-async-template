import pytest

from src.data_access import UserAsyncDataAccess
from src.schemas import RegisterSchema
from src.services.exceptions import AlreadyExists
from src.services.user import register_user


@pytest.mark.asyncio
async def test_register_user(
    user_data_access: UserAsyncDataAccess,
    register_schema: RegisterSchema,
):
    user = await register_user(user_data_access, register_schema)

    assert user.email == register_schema.email


@pytest.mark.asyncio
async def test_user_cannot_use_taken_email(
    user_data_access: UserAsyncDataAccess,
    register_schema: RegisterSchema,
):
    await register_user(user_data_access, register_schema)

    with pytest.raises(AlreadyExists):
        await register_user(user_data_access, register_schema)
