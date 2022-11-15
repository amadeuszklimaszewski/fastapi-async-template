import uuid

from sqlalchemy import Column, DateTime, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

from src.models.user import User

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
    Column("email", String(), nullable=True),
    Column("password", String(), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)


def start_mappers():
    mapper_registry.map_imperatively(User, users)
