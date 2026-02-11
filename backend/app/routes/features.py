"""Routes for feature plan generation."""
import json
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    FeaturePlanRequest,
    FeaturePlanResponse,
    FeaturePlanUpdate,
    FeaturePlanListResponse,
    EngineeringTask,
    UserStory,
)
from ..services.feature_service import FeatureService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/features", tags=["features"])


@router.post("/generate", response_model=FeaturePlanResponse)
async def generate_feature_plan(
    request: FeaturePlanRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a new feature plan.
    
    Takes a goal, list of users, and constraints, then generates:
    - User stories
    - Engineering tasks grouped by category
    - Risks and mitigations
    """
    try:
        plan = FeatureService.generate_plan(
            goal=request.goal,
            users=request.users,
            constraints=request.constraints,
            db=db
        )

        # Parse and return
        return FeaturePlanResponse(
            id=plan.id,
            goal=plan.goal,
            user_stories=[
                UserStory(**story)
                for story in json.loads(plan.user_stories)
            ],
            engineering_tasks={
                category: [
                    EngineeringTask(**task)
                    for task in tasks
                ]
                for category, tasks in json.loads(plan.engineering_tasks).items()
            },
            risks=json.loads(plan.risks),
            created_at=plan.created_at
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/recent", response_model=list[FeaturePlanListResponse])
async def get_recent_plans(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get the last N feature plans."""
    try:
        plans = FeatureService.get_recent_plans(db, limit=limit)
        return plans
    except Exception as e:
        logger.error(f"Error fetching recent plans: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{plan_id}", response_model=FeaturePlanResponse)
async def get_feature_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific feature plan by ID."""
    try:
        plan = FeatureService.get_plan_by_id(plan_id, db)
        if not plan:
            raise HTTPException(status_code=404, detail="Feature plan not found")

        return FeaturePlanResponse(
            id=plan.id,
            goal=plan.goal,
            user_stories=[
                UserStory(**story)
                for story in json.loads(plan.user_stories)
            ],
            engineering_tasks={
                category: [
                    EngineeringTask(**task)
                    for task in tasks
                ]
                for category, tasks in json.loads(plan.engineering_tasks).items()
            },
            risks=json.loads(plan.risks),
            created_at=plan.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching plan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{plan_id}/tasks")
async def update_plan_tasks(
    plan_id: int,
    request: FeaturePlanUpdate,
    db: Session = Depends(get_db)
):
    """Update engineering tasks for a plan."""
    try:
        plan = FeatureService.update_plan_tasks(
            plan_id=plan_id,
            engineering_tasks=request.engineering_tasks,
            db=db
        )
        if not plan:
            raise HTTPException(status_code=404, detail="Feature plan not found")

        return {
            "message": "Tasks updated successfully",
            "plan_id": plan_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{plan_id}/export")
async def export_as_markdown(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """Export feature plan as markdown."""
    try:
        plan = FeatureService.get_plan_by_id(plan_id, db)
        if not plan:
            raise HTTPException(status_code=404, detail="Feature plan not found")

        user_stories = json.loads(plan.user_stories)
        engineering_tasks = json.loads(plan.engineering_tasks)
        risks = json.loads(plan.risks)

        markdown = f"""# Feature Plan

## Goal
{plan.goal}

## User Stories
"""
        for story in user_stories:
            markdown += f"""
### {story['title']}
{story['description']}

**Acceptance Criteria:**
"""
            for criterion in story.get('acceptance_criteria', []):
                markdown += f"- {criterion}\n"

        markdown += "\n## Engineering Tasks\n"
        for category, tasks in engineering_tasks.items():
            markdown += f"\n### {category}\n"
            for task in tasks:
                markdown += f"""
- **{task['title']}** ({task.get('priority', 'Medium')} | {task.get('estimated_effort', 'TBD')})
  - {task.get('description', 'N/A')}
"""

        markdown += "\n## Risks\n"
        for risk in risks:
            markdown += f"""
- **{risk.get('risk', 'N/A')}**
  - Mitigation: {risk.get('mitigation', 'N/A')}
  - Severity: {risk.get('severity', 'Medium')}
"""

        return {
            "content": markdown,
            "filename": f"feature_plan_{plan_id}.md"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting plan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
