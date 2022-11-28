import datetime

from src.models import BaseUUIDModel


class User(BaseUUIDModel):
    email: str
    password: str
