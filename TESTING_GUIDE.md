# Testing Guide - Tasks Generator

## Pre-Deployment Testing

### 1. Environment Setup Test

```bash
# Check Python version
python --version          # Should be 3.11+

# Check Node version
node --version           # Should be 18+

# Check Docker (if using containers)
docker --version
docker-compose --version
```

### 2. Backend Health Check

After starting backend with: `python -m uvicorn app.main:app --reload`

**Test 1: Root Endpoint**
```bash
curl http://localhost:8000
```
Expected: JSON response with app info

**Test 2: API Docs**
Open: `http://localhost:8000/docs`
Expected: Interactive API documentation page

**Test 3: Health Check**
```bash
curl http://localhost:8000/api/health/status
```
Expected: JSON with status "healthy", backend, database, and llm status

**Test 4: Health Ping**
```bash
curl http://localhost:8000/api/health/ping
```
Expected: `{"message":"pong","timestamp":"..."}`

### 3. Frontend Health Check

After starting frontend with: `npm run dev`

Visit: `http://localhost:5173`
Expected: App loads with form visible

### 4. API Integration Test

**Test 4a: Generate Feature Plan**
```bash
curl -X POST http://localhost:8000/api/features/generate \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a simple TODO app",
    "users": ["Student", "Teacher"],
    "constraints": ["2 weeks", "$1000"]
  }'
```

Expected: JSON response with:
- id (integer)
- goal (string)
- user_stories (array)
- engineering_tasks (object with categories)
- risks (array)
- created_at (datetime)

**Test 4b: Get Recent Plans**
```bash
curl http://localhost:8000/api/features/recent?limit=5
```

Expected: Array of recent plans

**Test 4c: Get Specific Plan**
```bash
curl http://localhost:8000/api/features/1
```

Expected: Single plan details (if ID 1 exists)

**Test 4d: Update Tasks**
```bash
curl -X PUT http://localhost:8000/api/features/1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "engineering_tasks": {
      "Frontend": [
        {
          "id": "FE-001",
          "title": "Build Login Component",
          "description": "Create login page",
          "category": "Frontend",
          "priority": "High",
          "estimated_effort": "2 days",
          "order": 0
        }
      ],
      "Backend": []
    }
  }'
```

Expected: Success message

**Test 4e: Export as Markdown**
```bash
curl http://localhost:8000/api/features/1/export
```

Expected: JSON with markdown content and filename

---

## UI/UX Testing

### Feature Form Testing

1. **Empty form submission**
   - Click "Generate"
   - Expected: Validation errors for all fields

2. **Partial form submission**
   - Fill only goal
   - Expected: Error asking for users and constraints

3. **Valid submission**
   - Fill goal: "Build e-commerce platform"
   - Add users: "Customer", "Admin"
   - Add constraints: "3 months", "Team of 5"
   - Click "Generate Feature Plan"
   - Expected: Loading spinner, then plan displays

4. **Add/Remove functionality**
   - Click "+ Add User" multiple times
   - Click "✕" to remove
   - Expected: Dynamic list updates

### Plan View Testing

1. **Plan displays**
   - Goal visible at top
   - User stories displayed with criteria
   - Tasks grouped by category
   - Risks shown with severity

2. **Task reordering**
   - Click "↑ Move Up" on a task
   - Expected: Task moves up in list
   - Click "↓ Move Down"
   - Expected: Task moves down

3. **Save changes**
   - Reorder tasks
   - Click "Save Changes"
   - Expected: Success message
   - Go back and re-open plan
   - Expected: Changes persist

4. **Export markdown**
   - Click "Export as Markdown"
   - Expected: File downloads with plan content

### Health Status Testing

1. **Check health indicator**
   - Should show at top of page
   - All statuses should be green (healthy)
   - Click after 30 seconds
   - Expected: Timestamp updates

2. **Simulate failures** (optional)
   - Stop backend
   - Expected: Health status shows degraded
   - Start backend again
   - Expected: Status returns to healthy

### Recent Plans Testing

1. **View recent plans**
   - Generate multiple plans
   - Expected: List shows up to 5 recent plans
   - Click a plan
   - Expected: Plan details load

2. **Navigation**
   - Click recent plan
   - Verify plan loads correctly
   - Click "← Back to Form"
   - Expected: Return to form

---

## Error Scenario Testing

### Backend Error Cases

1. **Invalid JSON**
```bash
curl -X POST http://localhost:8000/api/features/generate \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```
Expected: 400 Bad Request

2. **Missing required fields**
```bash
curl -X POST http://localhost:8000/api/features/generate \
  -H "Content-Type: application/json" \
  -d '{"goal": "Test"}'
```
Expected: 400 with validation error

3. **Nonexistent plan**
```bash
curl http://localhost:8000/api/features/99999
```
Expected: 404 Not Found

4. **Invalid plan ID format**
```bash
curl http://localhost:8000/api/features/abc
```
Expected: 422 Unprocessable Entity

### Frontend Error Cases

1. **API unreachable**
   - Stop backend
   - Try to generate plan
   - Expected: Error message displayed

2. **Network timeout**
   - Simulate slow network (browser DevTools)
   - Generate plan
   - Expected: Loading state visible

3. **Invalid response**
   - Modify API response (use developer tools)
   - Expected: Graceful error handling

---

## Performance Testing

### Load Testing

1. **Multiple rapid requests**
```bash
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/features/generate \
    -H "Content-Type: application/json" \
    -d '{
      "goal": "Test goal '$i'",
      "users": ["User1", "User2"],
      "constraints": ["Constraint1", "Constraint2"]
    }' &
done
wait
```
Expected: All requests complete successfully

2. **Large payload**
   - 10 users and 10 constraints
   - Expected: Still generates correctly

3. **Frontend responsiveness**
   - Generate plan
   - UI remains responsive
   - Can click buttons while loading

---

## Database Testing

### 1. Data Persistence

1. **Generate a plan**
2. **Restart application**
3. **Check recent plans**
   - Expected: Previously generated plan still exists

### 2. Data Integrity

```bash
# Get a plan and verify all fields are present
curl http://localhost:8000/api/features/1 | jq .
```

Expected output includes:
- id, goal, user_stories, engineering_tasks, risks, created_at

### 3. Database file

Check that `tasks_generator.db` exists and grows:
```bash
ls -lh tasks_generator.db     # Linux/Mac
dir tasks_generator.db        # Windows
```

---

## Docker Testing

### 1. Container Build Test

```bash
docker-compose build
```
Expected: Both backend and frontend images build successfully

### 2. Container Run Test

```bash
docker-compose up
```
Expected:
- Backend starts and logs "Uvicorn running"
- Frontend starts and logs "Local: http://localhost..."
- Both containers report healthy in health checks

### 3. Container Communication

- Frontend should connect to backend
- API calls should work through container network
- Database persists in volume

### 4. Stop and Cleanup

```bash
docker-compose down
```
Expected: All containers stop gracefully

---

## Integration Testing Checklist

- [ ] Backend server starts without errors
- [ ] Frontend app loads in browser
- [ ] Health check shows all systems healthy
- [ ] Can generate a feature plan
- [ ] Plan data displays correctly
- [ ] Can edit and reorder tasks
- [ ] Can save changes
- [ ] Can export as markdown
- [ ] Recent plans display correctly
- [ ] Can select and view recent plans
- [ ] Error messages display appropriately
- [ ] Docker containers build and run
- [ ] Database persists data
- [ ] CORS works between frontend and backend

---

## Regression Testing

After making changes, verify:

1. **Form submission** still works
2. **Plan generation** produces valid JSON
3. **Database queries** return correct data
4. **Export functionality** generates valid markdown
5. **Health check** reports accurate status
6. **UI components** render without errors
7. **API endpoints** return proper status codes
8. **Error handling** works as expected

---

## Browser Compatibility Testing

Test with:
- Chrome/Chromium
- Firefox
- Safari (Mac)
- Edge (Windows)

Expected: App works consistently across browsers

---

## Performance Benchmarks

Acceptable ranges:
- **API response time**: < 2 seconds
- **Frontend load time**: < 3 seconds
- **Database query**: < 100ms
- **LLM response time**: 5-15 seconds

---

## Stress Testing

Monitor under load:
- Memory usage: Should stay below 500MB
- CPU usage: Should peak below 50%
- Database size: Grows as expected

---

## Final Verification

Before production deployment, verify:

✅ All endpoints return correct status codes
✅ All error cases handled gracefully
✅ Database schema created correctly
✅ Environment variables configured
✅ API documentation accessible
✅ Health check reporting accurately
✅ Frontend and backend communicate
✅ Docker images build successfully
✅ All tests pass
✅ No console errors or warnings

---

## Test Results Template

Use this to document your testing:

```markdown
# Testing Results - [Date]

## Backend Tests
- Health Check: PASS / FAIL
- API Endpoints: PASS / FAIL
- Database: PASS / FAIL
- Error Handling: PASS / FAIL

## Frontend Tests
- Form Submission: PASS / FAIL
- Plan Display: PASS / FAIL
- Task Management: PASS / FAIL
- Export Functionality: PASS / FAIL

## Integration Tests
- End-to-End Flow: PASS / FAIL
- Recent Plans: PASS / FAIL
- Health Status: PASS / FAIL

## Docker Tests
- Build: PASS / FAIL
- Run: PASS / FAIL
- Communication: PASS / FAIL

## Issues Found
- [List any issues]

## Ready for Deployment
YES / NO
```

---

Happy Testing! 🧪
