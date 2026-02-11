"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class FeaturePlanRequest(BaseModel):
    """Request to generate a feature plan."""

    goal: str = Field(..., min_length=1, max_length=500)
    users: list[str] = Field(..., min_items=1, max_items=10)
    constraints: list[str] = Field(..., min_items=1, max_items=10)

    @validator("goal")
    def goal_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Goal cannot be empty")
        return v.strip()

    @validator("users", "constraints", pre=True)
    def validate_lists(cls, v):
        if not isinstance(v, list):
            raise ValueError("Must be a list")
        return [str(item).strip() for item in v if str(item).strip()]


class UserStory(BaseModel):
    """User story model."""

    title: str
    description: str
    acceptance_criteria: list[str]


class EngineeringTask(BaseModel):
    """Engineering task model."""

    id: str
    title: str
    description: str
    category: str  # Frontend, Backend, Database, Infrastructure, etc.
    priority: str  # High, Medium, Low
    estimated_effort: str  # e.g., "3-5 days"
    order: int = 0


class FeaturePlanResponse(BaseModel):
    """Generated feature plan response."""

    id: int
    goal: str
    user_stories: list[UserStory]
    engineering_tasks: dict[str, list[EngineeringTask]]  # grouped by category
    risks: list[dict]  # [{"risk": str, "mitigation": str}]
    created_at: datetime

    class Config:
        from_attributes = True


class FeaturePlanUpdate(BaseModel):
    """Update request for feature plan tasks."""

    engineering_tasks: dict[str, list[EngineeringTask]]


class FeaturePlanListResponse(BaseModel):
    """List response for recent feature plans."""

    id: int
    goal: str
    created_at: datetime

    class Config:
        from_attributes = True


class HealthStatus(BaseModel):
    """Health check status."""

    status: str  # "healthy", "degraded", "unhealthy"
    backend: dict  # {"status": str, ...}
    database: dict  # {"status": str, ...}
    llm: dict  # {"status": str, ...}
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    error_code: Optional[str] = None
