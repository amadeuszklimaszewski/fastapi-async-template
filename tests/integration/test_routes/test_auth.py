import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.models import User


@pytest.mark.asyncio
async def test_user_can_login(
    client: AsyncClient,
    user_in_db: User,
    user_login_data: dict[str, str],
):
    response: Response = await client.post("/auth/login/", data=user_login_data)

    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert len(response_body) == 2
    assert "access_token" in response_body
    assert "token_type" in response_body
    assert response_body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_cannot_login_with_wrong_password(
    client: AsyncClient,
    user_in_db: User,
    user_login_data: dict[str, str],
):
    user_login_data["password"] = "incorrect_password"
    response: Response = await client.post("/auth/login/", data=user_login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert "detail" in response_body
    assert response_body["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_user_cannot_login_with_non_existing_email(
    client: AsyncClient,
    user_login_data: dict[str, str],
):
    response: Response = await client.post("/auth/login/", data=user_login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert "detail" in response_body
    assert response_body["detail"] == "Incorrect email or password"
