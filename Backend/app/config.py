import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, RedisDsn, SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
IS_DEV = os.getenv("ENVIRONMENT", "dev") == "dev"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env" if IS_DEV else None,
        env_file_encoding="utf-8",
        extra="forbid" if not IS_DEV else "ignore",
        case_sensitive=False,
    )

    environment: str = "dev"
    postgres_host: str = "postgres"
    postgres_db: str = "doc_intel"
    postgres_user: str = "doc_intel"
    postgres_password: SecretStr = Field(min_length=12)
    redis_url: RedisDsn = "redis://redis:6379/0"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()