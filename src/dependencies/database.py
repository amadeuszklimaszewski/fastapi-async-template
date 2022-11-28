from src.adapters.orm import AsyncSession, async_session


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()
