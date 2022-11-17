import datetime

from src.models import BaseUUIDModel


class User(BaseUUIDModel):
    email: str
    password: str
    created_at: datetime.date
    updated_at: datetime.date
