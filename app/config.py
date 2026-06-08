from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings loaded from environment / app/.env."""

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    scrape_timeout_seconds: int = 15
    scrape_max_chars: int = 2_000

    model_config = SettingsConfigDict(
        env_file=_APP_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
