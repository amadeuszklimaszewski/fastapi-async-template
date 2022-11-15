import datetime

from src.models.abstract import UUIDBaseModel


class User(UUIDBaseModel):
    email: str
    password: str
    created_at: datetime.date
    updated_at: datetime.date
