"""Business logic for feature plan generation."""
import json
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models import FeaturePlan
from app.schemas import EngineeringTask, UserStory
from app.utils.llm import generate_feature_plan
from app.utils.validators import validate_feature_plan_input

logger = logging.getLogger(__name__)


class FeatureService:
    """Service for managing feature plans."""

    @staticmethod
    def generate_plan(
        goal: str,
        users: list[str],
        constraints: list[str],
        db: Session
    ) -> Optional[FeaturePlan]:
        """Generate a new feature plan."""
        # Validate input
        is_valid, error_msg = validate_feature_plan_input(goal, users, constraints)
        if not is_valid:
            logger.error(f"Validation error: {error_msg}")
            raise ValueError(error_msg)

        logger.info(f"Generating feature plan for goal: {goal}")

        # Call LLM
        plan_data = generate_feature_plan(goal, users, constraints)
        if not plan_data:
            logger.error("LLM failed to generate plan")
            raise RuntimeError("Failed to generate feature plan from LLM")

        # Create database record
        try:
            feature_plan = FeaturePlan(
                goal=goal,
                users=json.dumps(users),
                constraints=json.dumps(constraints),
                user_stories=json.dumps(plan_data.get("user_stories", [])),
                engineering_tasks=json.dumps(plan_data.get("engineering_tasks", {})),
                risks=json.dumps(plan_data.get("risks", []))
            )
            db.add(feature_plan)
            db.commit()
            db.refresh(feature_plan)
            logger.info(f"Feature plan created with id: {feature_plan.id}")
            return feature_plan
        except Exception as e:
            db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise

    @staticmethod
    def get_recent_plans(db: Session, limit: int = 5) -> list[FeaturePlan]:
        """Get recent feature plans."""
        return db.query(FeaturePlan).order_by(FeaturePlan.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_plan_by_id(plan_id: int, db: Session) -> Optional[FeaturePlan]:
        """Get a specific feature plan."""
        return db.query(FeaturePlan).filter(FeaturePlan.id == plan_id).first()

    @staticmethod
    def update_plan_tasks(
        plan_id: int,
        engineering_tasks: dict,
        db: Session
    ) -> Optional[FeaturePlan]:
        """Update engineering tasks for a plan."""
        plan = FeatureService.get_plan_by_id(plan_id, db)
        if not plan:
            logger.error(f"Plan not found: {plan_id}")
            return None

        try:
            plan.engineering_tasks = json.dumps(engineering_tasks)
            db.commit()
            db.refresh(plan)
            logger.info(f"Plan {plan_id} updated successfully")
            return plan
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating plan: {str(e)}")
            raise
