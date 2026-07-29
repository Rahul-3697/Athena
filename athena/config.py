"""
Application configuration for Project Athena.

This module is the single source of truth for all configurable
application settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Project Athena"
    app_version: str = "0.1.0"

    openai_api_key: str
    openai_model: str = "gpt-4"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()