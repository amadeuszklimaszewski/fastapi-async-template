from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.data_access import UserAsyncDataAccess
from src.dependencies.user import get_user_data_access
from src.models import AccessTokenData
from src.services.exceptions import InvalidCredentials
from src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = InvalidCredentials("Invalid credentials provided")


def decode_jwt_token(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.AUTH_SECRET_KEY, algorithms=[settings.HASHING_ALGORITHM]
        )
        if not payload:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload


def get_access_token_data(
    payload: dict[str, Any] = Depends(decode_jwt_token)
) -> AccessTokenData:
    return AccessTokenData(**payload)


async def get_current_user(
    data_access: UserAsyncDataAccess = Depends(get_user_data_access),
    token: AccessTokenData = Depends(get_access_token_data),
):
    user = data_access.get(token.id)
    if user is None:
        raise credentials_exception

    return user
