"""Main FastAPI application."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .routes import features, health
from .utils.logger import logger

settings = get_settings()


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting Tasks Generator API")
    
    # Validate settings
    errors = settings.validate()
    if errors:
        for error in errors:
            logger.warning(f"Configuration warning: {error}")
    
    # Initialize database
    init_db()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Tasks Generator API")


# Create FastAPI app
app = FastAPI(
    title="Tasks Generator API",
    description="Generate comprehensive feature plans using AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(features.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Tasks Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )
