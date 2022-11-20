import datetime

from src.models import BaseUUIDModel


class User(BaseUUIDModel):
    email: str
    password: str
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
