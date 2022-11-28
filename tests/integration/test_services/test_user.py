import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.data_access import UserAsyncDataAccess
from src.services import UserService
from src.schemas import RegisterSchema
from src.services.exceptions import AlreadyExists, InvalidCredentials
import pytest_asyncio
from src.models import User
from src.utils import pwd_context


@pytest.fixture
def user_data_access(session: AsyncSession) -> UserAsyncDataAccess:
    return UserAsyncDataAccess(session)


@pytest.fixture
def user_service(user_data_access: UserAsyncDataAccess) -> UserService:
    return UserService(user_data_access)


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
async def test_register_user(
    user_service: UserService,
    register_schema: RegisterSchema,
):

    user = await user_service.register_user(register_schema)

    assert user.email == register_schema.email


@pytest.mark.asyncio
async def test_user_cannot_use_taken_email(
    user_service: UserService,
    register_schema: RegisterSchema,
):
    await user_service.register_user(register_schema)

    with pytest.raises(AlreadyExists):
        await user_service.register_user(register_schema)


@pytest.mark.asyncio
async def test_authenticate_user(
    user_in_db: User,
    user_service: UserService,
):
    user = await user_service.authenticate(
        email=user_in_db.email, password="password123"
    )

    assert user.email == user_in_db.email


@pytest.mark.asyncio
async def test_invalid_credentials_exception(
    user_in_db: User,
    user_service: UserService,
):
    with pytest.raises(InvalidCredentials):
        await user_service.authenticate(
            email=user_in_db.email, password="incorrect_password"
        )

    with pytest.raises(InvalidCredentials):
        await user_service.authenticate(
            email="incorrect@example.com", password="password123"
        )
