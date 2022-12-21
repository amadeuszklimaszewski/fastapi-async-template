from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    AUTH_SECRET_KEY: str
    HASHING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_TIME: int = 30 * 60  # 30 minutes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
