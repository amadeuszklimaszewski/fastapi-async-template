import json

from fastapi import Depends
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.exceptions import InvalidCredentials
from src.database.connection import get_db
from src.models.user import User


async def authenticate_user(
    auth_jwt: AuthJWT = Depends(), session: AsyncSession = Depends(get_db)
) -> User:
    auth_jwt.jwt_required()
    user = json.loads(auth_jwt.get_jwt_subject())
    result = await session.execute(select(User).where(User.id == user["id"]))
    user = result.first()

    if user is None:
        raise InvalidCredentials("Invalid credentials provided.")

    return user
