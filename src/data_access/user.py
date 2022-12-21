from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.adapters.orm import mapper_registry
from src.data_access.exceptions import DoesNotExist
from src.data_access.sqlalchemy import SQLAlchemyAsyncDataAccess, SQLAlchemyDAO
from src.models import User


@mapper_registry.mapped
class UserDAO(SQLAlchemyDAO):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class UserAsyncDataAccess(SQLAlchemyAsyncDataAccess):
    @property
    def _dao(self) -> UserDAO:
        return UserDAO

    @property
    def _model(self) -> User:
        return User

    async def get_by_email(self, email: str) -> User | None:
        result = await self._async_session.scalar(
            select(self._dao).where(self._dao.email == email).limit(1)
        )
        if not result:
            return None
        return self._model.from_orm(result)
