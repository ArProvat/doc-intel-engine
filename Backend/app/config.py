from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    postgres_host: str = "postgres"
    postgres_db: str = "doc_intel"
    postgres_user: str = "doc_intel"
    postgres_password: SecretStr
    redis_url: str = "redis://redis:6379/0"


settings = Settings()
