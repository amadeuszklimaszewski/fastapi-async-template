from fastapi_another_jwt_auth import AuthJWT
from src.settings.database import DatabaseSettings
from src.settings.jwt import AuthJWTSettings


class Settings(AuthJWTSettings, DatabaseSettings):
    class Config:
        env_file = ".env"


settings = Settings()


@AuthJWT.load_config
def get_config() -> Settings:
    return settings
