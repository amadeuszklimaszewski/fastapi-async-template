from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from src.data_access import UserAsyncDataAccess
from src.models import User
from src.services.exceptions import InvalidCredentials
from src.settings import settings
from src.utils import verify_password


async def authenticate_user(
    data_access: UserAsyncDataAccess, email: str, password: str
) -> User:
    user = await data_access.get_by_email(email)
    if not user or not verify_password(password, user.password):
        raise InvalidCredentials("Invalid credentials provided")
    return user


def create_access_token(
    data: dict[str, Any], expire_in: int = settings.ACCESS_TOKEN_EXPIRE_TIME
) -> str:
    expire = datetime.utcnow() + timedelta(seconds=expire_in)

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.HASHING_ALGORITHM
    )
    return encoded_jwt
