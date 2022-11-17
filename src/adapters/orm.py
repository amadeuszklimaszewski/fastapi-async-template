import uuid
from abc import abstractmethod
from typing_extensions import Self
from datetime import datetime
from sqlalchemy import MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy.sql import func
from src.models.abstract import UUIDBaseModel

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


class BaseDAO:
    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    @classmethod
    def from_model(cls, model: UUIDBaseModel) -> Self:
        return cls(**model.dict())


@mapper_registry.mapped
class UserDAO(BaseDAO):
    __tablename__ = "users"

    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
