# Prompts Used

## System Prompt for Feature Plan Generation

```
You are a senior product manager with 15+ years of experience.
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
```

## User Prompt Template

```
Generate a feature plan for:

Goal: {goal}

User Personas:
- {users joined with newline}

Constraints:
- {constraints joined with newline}

Return ONLY valid JSON.
```

## Example Usage

### Input
```json
{
  "goal": "Build an e-commerce recommendation engine using ML",
  "users": [
    "Product Manager looking to increase conversions",
    "Data Scientist implementing ML models",
    "Frontend Developer building UI components"
  ],
  "constraints": [
    "Must be completed within 8 weeks",
    "Budget limited to $50k",
    "Team size: 5 people"
  ]
}
```

### Expected Output Structure
```json
{
  "user_stories": [
    {
      "title": "Personalized Product Recommendations",
      "description": "As a shopper, I want to see personalized product recommendations based on my browsing history...",
      "acceptance_criteria": [
        "Recommendations load within 2 seconds",
        "Accuracy of recommendations is >75%",
        "Mobile and desktop displays are optimized"
      ]
    },
    ...
  ],
  "engineering_tasks": {
    "Frontend": [
      {
        "id": "FE-001",
        "title": "Build Recommendation Widget Component",
        "description": "Create reusable React component for displaying product recommendations...",
        "priority": "High",
        "estimated_effort": "3-4 days"
      },
      ...
    ],
    "Backend": [
      {
        "id": "BE-001",
        "title": "Implement ML Model API Endpoint",
        "description": "Create REST endpoint that accepts user history and returns recommendations...",
        "priority": "High",
        "estimated_effort": "5-6 days"
      },
      ...
    ],
    "Database": [
      {
        "id": "DB-001",
        "title": "Optimize Product Embeddings Table",
        "description": "Index and optimize vectors table for fast similarity search...",
        "priority": "Medium",
        "estimated_effort": "2-3 days"
      },
      ...
    ],
    "Infrastructure": [
      {
        "id": "INF-001",
        "title": "Setup ML Model Serving Infrastructure",
        "description": "Configure TensorFlow Serving or similar for model inference...",
        "priority": "High",
        "estimated_effort": "3-4 days"
      }
    ]
  },
  "risks": [
    {
      "risk": "ML model accuracy may not meet 75% target",
      "mitigation": "Start with ensemble models, implement A/B testing to validate",
      "severity": "High"
    },
    {
      "risk": "Performance degradation under high user load",
      "mitigation": "Implement caching layer, load testing before production",
      "severity": "Medium"
    },
    {
      "risk": "Data privacy concerns with user behavior tracking",
      "mitigation": "Implement GDPR compliance, allow users to opt-out",
      "severity": "High"
    }
  ]
}
```

## Prompt Refinement Iterations

### Version 1 (Initial)
- Too open-ended, inconsistent JSON output
- LLM sometimes mixed markdown and JSON
- Missing structured fields

### Version 2 (With Structure)
- Added explicit field definitions
- Required minimum content (3 user stories)
- Still had occasional markdown wrapping

### Version 3 (Final - Current)
- Explicit "ONLY valid JSON" instruction
- Category examples with brackets []
- Regex parsing to extract JSON from markdown
- Up to 3 retry attempts for parsing

## Error Handling for LLM Responses

1. **JSON Parsing Failure**: Retry up to 3 times
2. **Missing Fields**: Log error and return None
3. **Invalid Structure**: Validate against schema before storing
4. **API Rate Limit**: Exponential backoff (implement for production)

## Future Prompt Improvements

1. **Few-shot Learning**: Include examples in system prompt
2. **Constraint Handling**: More explicit deadline/budget handling
3. **Cross-functional Tasks**: Better identification of dependencies
4. **Risk Severity**: More precise severity classification
5. **Effort Estimation**: Standardized effort points or hours

## Testing Prompts Locally

Use the OpenAI Playground to test prompts:
```bash
# Test system prompt and user input
POST https://api.openai.com/v1/chat/completions
{
  "model": "gpt-4-turbo",
  "messages": [
    {"role": "system", "content": "[SYSTEM_PROMPT]"},
    {"role": "user", "content": "[USER_PROMPT]"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```
