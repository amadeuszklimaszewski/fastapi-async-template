from datetime import datetime
from typing import Optional
import uuid as uuid_pkg
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, DateTime


class ModelBase(SQLModel):
    """
    Base class for database models.
    """

    id: Optional[int] = Field(default=None, primary_key=True)


class UUIDModelBase(SQLModel):
    """
    Base class for UUID-based models.
    """

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimeStampedUUIDModelBase(UUIDModelBase):
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), onupdate=datetime.utcnow, default=datetime.utcnow
        )
    )
