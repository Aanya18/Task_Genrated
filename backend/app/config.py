"""Configuration management for the application."""
import os
from functools import lru_cache
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./tasks_generator.db"
    )

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    # App
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")

    @property
    def is_database_sqlite(self) -> bool:
        """Check if using SQLite database."""
        return self.DATABASE_URL.startswith("sqlite")

    def validate(self) -> list[str]:
        """Validate required settings."""
        errors = []
        if not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY environment variable is not set")
        return errors


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
