"""LLM integration with Groq."""
import json
import logging
import re
from typing import Optional
from groq import Groq
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize Groq client lazily
_client = None

def get_client():
    """Get or create Groq client."""
    global _client
    if _client is None:
        try:
            _client = Groq(api_key=settings.GROQ_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise
    return _client


def generate_feature_plan(
    goal: str,
    users: list[str],
    constraints: list[str],
    max_retries: int = 3
) -> Optional[dict]:
    """
    Generate a feature plan using Groq API.
    
    Args:
        goal: The feature goal
        users: List of user personas
        constraints: List of constraints
        max_retries: Number of retries for JSON parsing
        
    Returns:
        Parsed feature plan dict or None if failed
    """
    system_prompt = """You are a senior product manager with 15+ years of experience.
Your task is to generate a comprehensive feature plan in STRICT JSON format.

The JSON must contain these exact keys:
{
    "user_stories": [{"title": str, "description": str, "acceptance_criteria": [str]}],
    "engineering_tasks": {
        "Frontend": [{"id": str, "title": str, "description": str, "priority": str, "estimated_effort": str}],
        "Backend": [{"id": str, "title": str, "description": str, "priority": str, "estimated_effort": str}],
        "Database": [...]
    },
    "risks": [{"risk": str, "mitigation": str, "severity": str}]
}

Requirements:
- At least 3 user stories
- Tasks grouped by category (Frontend, Backend, Database, Infrastructure)
- Each task has priority (High/Medium/Low) and effort estimate
- Return ONLY valid JSON, no markdown or extra text
- If a category has no tasks, use empty array []
"""

    user_content = f"""Generate a feature plan for:

Goal: {goal}

User Personas:
{chr(10).join(f'- {user}' for user in users)}

Constraints:
{chr(10).join(f'- {constraint}' for constraint in constraints)}

Return ONLY valid JSON."""

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Groq API (attempt {attempt + 1}/{max_retries})")
            
            response = get_client().chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON if wrapped in markdown
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            
            # Parse JSON
            plan = json.loads(content)
            
            # Validate structure
            if not all(key in plan for key in ["user_stories", "engineering_tasks", "risks"]):
                raise ValueError("Missing required keys in response")
            
            logger.info("Feature plan generated successfully")
            return plan
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed on attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to parse JSON after {max_retries} attempts")
                return None
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            return None
    
    return None


def check_llm_connection() -> bool:
    """Check if LLM connection is working."""
    try:
        logger.info("Testing LLM connection...")
        response = get_client().chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": "Say OK"}],
            temperature=0.1,
            max_tokens=10,
        )
        logger.info("LLM connection check passed")
        return True
    except Exception as e:
        logger.error(f"LLM connection check failed: {str(e)}")
        return False
