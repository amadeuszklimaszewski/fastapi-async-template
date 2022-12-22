import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.models import User


@pytest.fixture
def user_register_data() -> dict[str, str]:
    return {
        "email": "user@example.com",
        "password": "password123",
        "repeat_password": "password123",
    }


@pytest.mark.asyncio
async def test_user_can_register(
    client: AsyncClient,
    user_register_data: dict[str, str],
):
    response: Response = await client.post("/users/register/", json=user_register_data)

    assert response.status_code == status.HTTP_201_CREATED
    response_body = response.json()
    assert len(response_body) == 2
    assert "access_token" in response_body
    assert "token_type" in response_body
    assert response_body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_cannot_register_with_existing_email(
    client: AsyncClient,
    user_in_db: User,
    user_register_data: dict[str, str],
):
    response: Response = await client.post("/users/register/", json=user_register_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_body = response.json()
    assert len(response_body) == 1
    assert "detail" in response_body
    assert response_body["detail"] == "User with given email already exists"


@pytest.mark.asyncio
async def test_get_users(
    client: AsyncClient,
    user_in_db: User,
):
    response: Response = await client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert len(response_body) == 1
    assert "email" in response_body[0]
    assert response_body[0]["email"] == user_in_db.email
    assert response_body[0]["id"] == str(user_in_db.id)


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: AsyncClient,
    user_in_db: User,
):
    response: Response = await client.get(f"/users/{user_in_db.id}/")

    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert len(response_body) == 2
    assert "email" in response_body
    assert response_body["email"] == user_in_db.email
    assert response_body["id"] == str(user_in_db.id)
