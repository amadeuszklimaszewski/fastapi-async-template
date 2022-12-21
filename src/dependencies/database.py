from typing import AsyncIterable

from src.adapters.orm import AsyncSession, async_session


async def get_db() -> AsyncIterable[AsyncSession]:
    async with async_session() as session:
        yield session
        await session.commit()
