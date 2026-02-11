# Tasks Generator - Production-Ready Full-Stack Web App

A comprehensive web application for generating feature plans, user stories, and engineering tasks using AI (OpenAI ChatGPT).

## 🎯 Features

- **AI-Powered Feature Generation**: Uses OpenAI's GPT-4 Turbo to generate:
  - User Stories with acceptance criteria
  - Engineering tasks grouped by category (Frontend, Backend, Database, Infrastructure)
  - Risks and mitigation strategies
  
- **Task Management**: 
  - Edit and reorder engineering tasks
  - View last 5 feature plans
  - Export results as markdown
  
- **System Health Monitoring**:
  - Real-time backend status check
  - Database connection verification
  - LLM service connectivity test
  
- **Production-Ready**:
  - Docker containerization
  - Environment variable configuration
  - Comprehensive error handling
  - Structured logging
  - Input validation

## 📋 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **API**: RESTful with Pydantic validation
- **LLM**: OpenAI Chat Completion API
- **Web Server**: Uvicorn

### Frontend
- **Framework**: React 18 with Vite
- **HTTP Client**: Axios
- **Styling**: CSS3
- **Build Tool**: Vite

### Deployment
- **Containerization**: Docker & Docker Compose
- **Configuration**: Environment variables (.env)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key
- Docker (optional)

### Local Development Setup

#### 1. Clone and Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env
# Edit .env and add your OpenAI API key
```

#### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

#### 3. Run Locally

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the app at `http://localhost:5173`

### Docker Deployment

```bash
# Create .env file with your OpenAI API key
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
docker build -t tasks-generator-backend .
docker build -t tasks-generator-frontend ./frontend -f ./frontend/Dockerfile
```

Access the app at `http://localhost:3000`

## 📚 API Endpoints

### Feature Generation
- **POST** `/api/features/generate` - Generate new feature plan
  - Input: goal (string), users (array), constraints (array)
  - Returns: Complete feature plan with stories, tasks, and risks

### Feature Retrieval
- **GET** `/api/features/recent?limit=5` - Get last N feature plans
- **GET** `/api/features/{planId}` - Get specific feature plan
- **PUT** `/api/features/{planId}/tasks` - Update engineering tasks
- **GET** `/api/features/{planId}/export` - Export as markdown

### Health & Status
- **GET** `/api/health/status` - System health check
- **GET** `/api/health/ping` - Simple ping endpoint

## 📁 Project Structure

```
Task_Generators/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Settings & env vars
│   │   ├── database.py             # Database setup
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── features.py         # Feature endpoints
│   │   │   └── health.py           # Health check endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── feature_service.py  # Business logic
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py           # Logging setup
│   │       ├── llm.py              # OpenAI integration
│   │       └── validators.py       # Input validation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx            # Main page
│   │   │   └── Home.css
│   │   ├── components/
│   │   │   ├── FeatureForm.jsx     # Input form
│   │   │   ├── FeatureForm.css
│   │   │   ├── PlanView.jsx        # Plan display & edit
│   │   │   ├── PlanView.css
│   │   │   ├── Health.jsx          # Health status
│   │   │   ├── Health.css
│   │   │   ├── RecentPlans.jsx     # Recent plans list
│   │   │   └── RecentPlans.css
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── AI_NOTES.md
├── PROMPTS_USED.md
└── ABOUTME.md
```

## 🔑 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo
DATABASE_URL=sqlite:///./tasks_generator.db
DEBUG=False
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🎨 UI Features

- **Clean, responsive design** - Works on desktop and tablet
- **Real-time form validation** - Immediate user feedback
- **Color-coded task priorities** - Quick visual scanning
- **Dark mode health indicator** - System status at a glance
- **Markdown export** - Share plans easily
- **Recent plans sidebar** - Quick access to previous work

## 🛡️ Production Checklist

- [x] Input validation on all endpoints
- [x] Error handling with meaningful messages
- [x] Structured logging
- [x] Environment variables for secrets
- [x] Database migrations ready
- [x] Health check endpoints
- [x] CORS configuration
- [x] Docker support
- [x] Pydantic schema validation
- [x] SQLAlchemy ORM with proper sessions

## 🚦 Health Check System

The system monitors three critical components:

1. **Backend Service** - Application is running
2. **Database Connection** - SQLite/database is accessible
3. **LLM Service** - OpenAI API is reachable

Status is shown in the UI with real-time updates every 30 seconds.

## 📊 Data Models

### FeaturePlan
- `id`: Integer (Primary Key)
- `goal`: String (500 chars max)
- `users`: JSON array
- `constraints`: JSON array
- `user_stories`: JSON array with acceptance criteria
- `engineering_tasks`: JSON object grouped by category
- `risks`: JSON array with mitigations
- `created_at`: DateTime
- `updated_at`: DateTime

## 🔄 LLM Integration

The system uses OpenAI's Chat Completion API with:
- **Model**: GPT-4 Turbo (configurable)
- **Role**: Senior Product Manager
- **Output**: Strict JSON format with validation
- **Retry Logic**: Up to 3 attempts for JSON parsing failures

## 📝 Export Format

Generated plans are exportable as markdown with sections:
- Feature Goal
- User Stories (with acceptance criteria)
- Engineering Tasks (grouped by category)
- Risks (with severity and mitigation)

## 🐛 Error Handling

- Validation errors return 400 with detailed messages
- Not found errors return 404
- Server errors return 500 with logging
- LLM failures gracefully handled with retries
- Database connection errors are monitored

## 📜 License

This project is provided as-is for production use.

## 📧 Support

For issues or questions, refer to the generated AI_NOTES.md and PROMPTS_USED.md documentation.
