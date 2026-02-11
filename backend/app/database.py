"""Database configuration and session management."""
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create engine with appropriate pool settings
engine_kwargs = {}
if settings.is_database_sqlite:
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database by creating all tables."""
    from app.models import Base
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


def check_db_connection() -> bool:
    """Check if database connection is healthy."""
    try:
        with engine.connect() as conn:
            # SQLite specific check
            if settings.is_database_sqlite:
                conn.execute("SELECT 1")
            logger.info("Database connection check passed")
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False


def get_db_info() -> dict:
    """Get database information."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {
            "status": "connected",
            "tables": tables,
            "url": settings.DATABASE_URL
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "url": settings.DATABASE_URL
        }
