from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_ENGINE: str = "postgresql+asyncpg"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    LOGS_PATH: Path

    API_HOST: str
    API_PORT: int
    API_SECRET_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
