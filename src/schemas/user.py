import datetime
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field, validate_email, validator


class UserOutputSchema(BaseModel):
    id: UUID
    email: str
    created_at: datetime.date
    updated_at: datetime.date


class LoginSchema(BaseModel):
    email: str
    password: str


class RegisterSchema(BaseModel):
    email: str
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)

    @validator("email")
    def validate_email(cls, email: str) -> str:
        validate_email(email)
        return email

    @validator("repeat_password")
    def validate_password(cls, repeat_password: str, values: dict[str, Any]) -> str:
        if repeat_password != values["password"]:
            raise ValueError("Passwords do not match")
        return repeat_password
