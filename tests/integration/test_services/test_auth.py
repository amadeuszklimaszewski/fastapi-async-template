import pytest

from src.data_access import UserAsyncDataAccess
from src.models import User
from src.services.auth import authenticate_user
from src.services.exceptions import InvalidCredentials


@pytest.mark.asyncio
async def test_authenticate_user(
    user_data_access: UserAsyncDataAccess,
    user_in_db: User,
):
    user = await authenticate_user(
        user_data_access, email=user_in_db.email, password="password123"
    )

    assert user.email == user_in_db.email


@pytest.mark.asyncio
async def test_invalid_credentials_exception(
    user_data_access: UserAsyncDataAccess,
    user_in_db: User,
):
    with pytest.raises(InvalidCredentials):
        await authenticate_user(
            user_data_access, email=user_in_db.email, password="incorrect_password"
        )

    with pytest.raises(InvalidCredentials):
        await authenticate_user(
            user_data_access, email="incorrect@example.com", password="password123"
        )
