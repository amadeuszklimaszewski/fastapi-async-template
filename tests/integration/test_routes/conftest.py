import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access import UserAsyncDataAccess
from src.models import User
from src.utils import pwd_context


@pytest.fixture
def user_login_data() -> dict[str, str]:
    return {
        "grant_type": "password",
        "username": "user@example.com",
        "password": "password123",
    }


@pytest.fixture
def user_data_access(session: AsyncSession) -> UserAsyncDataAccess:
    return UserAsyncDataAccess(session)


@pytest_asyncio.fixture
async def user_in_db(
    user_data_access: UserAsyncDataAccess,
    user_login_data: dict[str, str],
) -> User:
    email = user_login_data["username"]
    password = pwd_context.hash(user_login_data["password"])
    user = User(email=email, password=password)

    await user_data_access.persist(user)
    return user
