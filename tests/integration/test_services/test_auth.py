import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access import UserAsyncDataAccess
from src.models import User
from src.schemas import RegisterSchema
from src.services.auth import authenticate_user
from src.services.exceptions import InvalidCredentials
from src.utils import pwd_context


@pytest.fixture
def user_data_access(session: AsyncSession) -> UserAsyncDataAccess:
    return UserAsyncDataAccess(session)


@pytest.fixture
def register_schema() -> RegisterSchema:
    return RegisterSchema(
        email="user@example.com",
        password="password123",
        repeat_password="password123",
    )


@pytest_asyncio.fixture
async def user_in_db(
    user_data_access: UserAsyncDataAccess,
    register_schema: RegisterSchema,
) -> User:
    email = register_schema.email
    password = pwd_context.hash(register_schema.password)
    user = User(email=email, password=password)

    await user_data_access.persist(user)
    return user


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
