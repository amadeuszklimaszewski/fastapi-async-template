from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import registry, sessionmaker

from src.settings import settings

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


engine = create_async_engine(settings.postgres_url, echo=False)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
