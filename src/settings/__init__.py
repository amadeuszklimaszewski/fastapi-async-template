from src.settings.database import DatabaseSettings


class Settings(DatabaseSettings):
    class Config:
        env_file = ".env"


settings = Settings()