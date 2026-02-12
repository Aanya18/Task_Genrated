"""Configuration management for the application."""
import os
from functools import lru_cache
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (from root directory)
dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path)


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./tasks_generator.db"
    )

    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3.1-8b-instant")

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
        if not self.GROQ_API_KEY:
            errors.append("GROQ_API_KEY environment variable is not set")
        return errors


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
