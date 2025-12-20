"""Application configuration management."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite+aiosqlite:///./trendresponse.db"

    # Redis
    redis_url: Optional[str] = None

    # GitHub Models
    github_token: str
    model_endpoint: str = "https://models.github.ai/inference/"
    model_name: str = "openai/gpt-4.1-mini"

    # LinkedIn OAuth
    linkedin_client_id: str
    linkedin_client_secret: str
    linkedin_redirect_uri: str = "http://localhost:8000/auth/linkedin/callback"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # Sentry
    sentry_dsn: Optional[str] = None

    # Comment constraints
    min_word_count: int = 10
    max_word_count: int = 25
    rate_limit_comments_per_minute: int = 1


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
