from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseUUIDModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True
