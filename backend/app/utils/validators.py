"""Input validation utilities."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def validate_feature_plan_input(goal: str, users: list[str], constraints: list[str]) -> tuple[bool, Optional[str]]:
    """
    Validate feature plan input.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate goal
    if not goal or not goal.strip():
        return False, "Goal cannot be empty"
    
    if len(goal) > 500:
        return False, "Goal must be less than 500 characters"
    
    # Validate users
    if not users or len(users) == 0:
        return False, "At least one user persona is required"
    
    if len(users) > 10:
        return False, "Maximum 10 user personas allowed"
    
    for user in users:
        if not user or not str(user).strip():
            return False, "User personas cannot be empty"
    
    # Validate constraints
    if not constraints or len(constraints) == 0:
        return False, "At least one constraint is required"
    
    if len(constraints) > 10:
        return False, "Maximum 10 constraints allowed"
    
    for constraint in constraints:
        if not constraint or not str(constraint).strip():
            return False, "Constraints cannot be empty"
    
    return True, None
