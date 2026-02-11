"""Database models using SQLAlchemy."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FeaturePlan(Base):
    """Feature plan generated from user specifications."""

    __tablename__ = "feature_plans"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String(500), nullable=False)
    users = Column(Text, nullable=False)  # JSON string
    constraints = Column(Text, nullable=False)  # JSON string
    user_stories = Column(Text, nullable=False)  # JSON string
    engineering_tasks = Column(Text, nullable=False)  # JSON string
    risks = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        """Pydantic config."""
        from_attributes = True
