"""Health check endpoints."""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db, check_db_connection
from app.schemas import HealthStatus
from app.utils.llm import check_llm_connection

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/status", response_model=HealthStatus)
async def health_check(db: Session = Depends(get_db)):
    """
    Check system health status.
    
    Verifies:
    - Backend service is running
    - Database connection
    - LLM service connection
    """
    backend_status = {"status": "healthy"}
    database_status = {
        "status": "healthy" if check_db_connection() else "unhealthy"
    }
    llm_status = {
        "status": "healthy" if check_llm_connection() else "unhealthy"
    }

    # Determine overall status
    all_healthy = all([
        backend_status["status"] == "healthy",
        database_status["status"] == "healthy",
        llm_status["status"] == "healthy"
    ])

    overall_status = "healthy" if all_healthy else "degraded"

    logger.info(f"Health check - Overall: {overall_status}, DB: {database_status['status']}, LLM: {llm_status['status']}")

    return HealthStatus(
        status=overall_status,
        backend=backend_status,
        database=database_status,
        llm=llm_status,
        timestamp=datetime.utcnow()
    )


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong", "timestamp": datetime.utcnow()}
