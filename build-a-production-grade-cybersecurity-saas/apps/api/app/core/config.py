from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://radar:radar@postgres:5432/radar"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = Field(default="change-me-in-production", min_length=16)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    RATE_LIMIT_PER_MINUTE: int = 120
    SCAN_RATE_LIMIT_PER_HOUR: int = 30
    CACHE_DEFAULT_TTL_SECONDS: int = 900
    REQUIRE_STRONG_SECRETS: bool = False

    def validate_production_security(self) -> None:
        if self.APP_ENV == "production" and self.REQUIRE_STRONG_SECRETS:
            if self.JWT_SECRET == "change-me-in-production" or len(self.JWT_SECRET) < 32:
                raise ValueError("JWT_SECRET must be changed to a strong random value in production")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
