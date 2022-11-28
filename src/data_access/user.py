from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.adapters.orm import mapper_registry
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
