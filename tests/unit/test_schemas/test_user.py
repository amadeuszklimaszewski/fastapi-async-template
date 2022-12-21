import pytest

from src.schemas import RegisterSchema


def test_register_schema_email_validation():
    with pytest.raises(ValueError):
        register_schema = RegisterSchema(
            email="incorrect_email",
            password="password123",
            repeat_password="password123",
        )


def test_register_schema_too_short_password_validation():
    with pytest.raises(ValueError):
        register_schema = RegisterSchema(
            email="email@example.com",
            password="short",
            repeat_password="short",
        )


def test_register_schema_passwords_mismatch_validation():
    with pytest.raises(ValueError):
        register_schema = RegisterSchema(
            email="email@example.com",
            password="password123",
            repeat_password="password321",
        )
