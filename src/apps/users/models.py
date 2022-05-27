import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import Any
from pydantic import validator, validate_email as validate_email_pd
from sqlmodel import SQLModel, Field, Column, String
from src.core.models import TimeStampedUUIDModelBase


class UserBase(SQLModel):
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    first_name: str
    last_name: str
    birthday: dt.date
    is_active: bool = True


class UserOutput(TimeStampedUUIDModelBase, UserBase):
    ...


class User(TimeStampedUUIDModelBase, UserBase, table=True):
    hashed_password: str


class LoginSchema(SQLModel):
    email: str
    password: str


class RegisterSchema(UserBase):
    password: str = Field(..., min_length=8)
    password2: str = Field(..., min_length=8)

    @validator("birthday")
    def validate_birthday(cls, birthday: dt.datetime) -> dt.datetime:
        if relativedelta(dt.date.today(), birthday).years <= 18:
            raise ValueError("You must be at least 18 years old")
        return birthday

    @validator("email")
    def validate_email(cls, email: str) -> str:
        validate_email_pd(email)
        return email

    @validator("password2")
    def validate_password(cls, password2: str, values: dict[str, Any]) -> str:
        if password2 != values["password"]:
            raise ValueError("Passwords do not match")
        return password2
