from fastapi import Response, status
from httpx import AsyncClient
import pytest
import pytest_asyncio
from fastapi_another_jwt_auth import AuthJWT
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apps.users.models import User, UserOutput, RegisterSchema
from src.apps.users.services import UserService


@pytest.fixture
def user_register_data() -> dict[str, str]:
    return {
        "first_name": "name",
        "last_name": "name",
        "username": "username",
        "email": "testuser@google.com",
        "password": "test12345",
        "password2": "test12345",
        "birthday": "2000-01-01",
    }


@pytest.fixture
def user_login_data() -> dict[str, str]:
    return {
        "email": "testuser@google.com",
        "password": "test12345",
    }


@pytest_asyncio.fixture
async def register_user(
    user_register_data: dict[str, str], session: AsyncSession
) -> UserOutput:
    schema = RegisterSchema(**user_register_data)
    return await UserService.register_user(schema=schema, session=session)


@pytest.fixture
def user_bearer_token_header(register_user: UserOutput) -> dict[str, str]:
    access_token = AuthJWT().create_access_token(subject=register_user.json())
    return {"Authorization": f"Bearer {access_token}"}


@pytest.mark.asyncio
async def test_user_can_login(
    client: AsyncClient,
    register_user: UserOutput,
    user_login_data: dict[str, str],
    session: AsyncSession,
):
    response: Response = await client.post("/users/login/", json=user_login_data)

    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert len(response_body) == 1


@pytest.mark.asyncio
async def test_user_can_register(
    client: AsyncClient,
    user_register_data: dict[str, str],
    session: AsyncSession,
):
    response: Response = await client.post("/users/register/", json=user_register_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert len((await session.exec(select(User))).all()) == 1
    assert (await session.exec(select(User))).first().username == user_register_data[
        "username"
    ]


@pytest.mark.asyncio
async def test_authenticated_user_can_get_users_list(
    client: AsyncClient,
    register_user: UserOutput,
    user_bearer_token_header: dict[str, str],
    session: AsyncSession,
):
    response: Response = await client.get("/users/", headers=user_bearer_token_header)
    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert len(response_body) == 1


@pytest.mark.asyncio
async def test_authenticated_user_can_get_his_profile(
    client: AsyncClient,
    register_user: UserOutput,
    user_bearer_token_header: dict[str, str],
    session: AsyncSession,
):
    response: Response = await client.get(
        "/users/profile/", headers=user_bearer_token_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == register_user.username
    assert response.json()["id"] == str(register_user.id)


@pytest.mark.asyncio
async def test_authenticated_user_can_get_his_profile_by_id(
    client: AsyncClient,
    register_user: UserOutput,
    user_bearer_token_header: dict[str, str],
    session: AsyncSession,
):
    response: Response = await client.get(
        f"/users/{register_user.id}/", headers=user_bearer_token_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == register_user.username
    assert response.json()["id"] == str(register_user.id)


@pytest.mark.asyncio
async def test_anonymous_user_cannot_get_users_list(
    client: AsyncClient,
    register_user: UserOutput,
    session: AsyncSession,
):
    response: Response = await client.get("/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


@pytest.mark.asyncio
async def test_anonymous_user_cannot_get_users_profile(
    client: AsyncClient,
    register_user: UserOutput,
    session: AsyncSession,
):
    response: Response = await client.get("/users/profile/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


@pytest.mark.asyncio
async def test_anonymous_user_cannot_get_users_profile_by_id(
    client: AsyncClient,
    register_user: UserOutput,
    session: AsyncSession,
):
    response: Response = await client.get(f"/users/{register_user.id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"
