from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    TEST_MODE: bool = False

    @property
    def postgres_url(self) -> str:
        database_name = (
            self.POSTGRES_DATABASE
            if not self.TEST_MODE
            else f"test{self.POSTGRES_DATABASE}"
        )

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{database_name}"
        )
