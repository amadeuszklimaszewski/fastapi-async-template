from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access import UserAsyncDataAccess
from src.dependencies.database import get_db


async def get_user_data_access(async_session: AsyncSession = Depends(get_db)):
    return UserAsyncDataAccess(async_session)
