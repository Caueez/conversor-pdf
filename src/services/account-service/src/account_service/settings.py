from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AccountSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    ENV: str = "dev"
    NAME: str = "account-service"
    DEBUG: bool = True

    PERSISTENCE_BACKEND: str = "postgres"
    CACHE_BACKEND: str = "redis"
    BROKER_BACKEND: str = "rabbitmq"
    
    POSTGRES_DSN: str = "postgresql://postgres:postgres@postgres:5432/user_service"
    REDIS_DSN: str = "redis://redis:6379/0"
    RABBITMQ_DSN: str = "amqp://guest:guest@rabbitmq:5672/"

    USER_REPO: str = "postgres"

    PASSWORD_HASHER_ROUNDS: int = 12


@lru_cache(maxsize=1)
def get_settings() -> AccountSettings:
    return AccountSettings()
