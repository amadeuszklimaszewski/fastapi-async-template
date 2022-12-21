from src.settings.auth import AuthSettings
from src.settings.database import DatabaseSettings


class Settings(AuthSettings, DatabaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
