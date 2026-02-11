# Setup Instructions

## Prerequisites

Before running the application, ensure you have:

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com
   - Create an API key in your account settings
   - Keep it secure (never commit to git)

2. **For Docker Deployment**
   - Docker Desktop (https://www.docker.com/products/docker-desktop)
   - Docker Compose (included with Docker Desktop)

3. **For Local Development**
   - Python 3.11+ (https://www.python.org/downloads/)
   - Node.js 18+ (https://nodejs.org/)
   - Git (https://git-scm.com/)

## Quick Start (Recommended)

### Using Docker Compose

```bash
# 1. Clone/navigate to the project
cd Task_Generators

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your OpenAI API key
# On Windows: notepad .env
# On Mac/Linux: nano .env
# Add your key: OPENAI_API_KEY=sk-your-api-key-here

# 4. Start the application
docker-compose up --build

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API Docs: http://localhost:8000/docs
```

### Using Startup Scripts

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

## Detailed Setup - Local Development

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Navigate back and set up .env
cd ..
cp .env.example .env
# Edit .env with your OpenAI API key

# 6. Start backend server
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

In a new terminal:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
cp .env.example .env

# 4. Start development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Configuration

### Environment Variables

**.env (Root)** - Backend configuration:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here    # Required!
OPENAI_MODEL=gpt-4-turbo                # LLM Model

# Database
DATABASE_URL=sqlite:///./tasks_generator.db

# Application
DEBUG=False
LOG_LEVEL=INFO

# CORS - Allowed origins for frontend
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**frontend/.env** - Frontend configuration:
```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api
```

## First Run Checklist

- [ ] OpenAI API key obtained and added to .env
- [ ] Python 3.11+ installed (for local development)
- [ ] Node.js 18+ installed (for local development)
- [ ] Docker installed (for Docker deployment)
- [ ] Backend running and accessible at http://localhost:8000
- [ ] Frontend running and accessible at http://localhost:5173
- [ ] Health check passing: http://localhost:8000/api/health/status

## Testing the Application

### 1. Check System Health

Visit: `http://localhost:8000/api/health/status`

Expected response:
```json
{
  "status": "healthy",
  "backend": {"status": "healthy"},
  "database": {"status": "healthy"},
  "llm": {"status": "healthy"},
  "timestamp": "2024-02-11T..."
}
```

### 2. Generate a Test Feature Plan

In the UI:
1. Enter a goal: "Build a task management app"
2. Add users: "Product Manager", "Developer"
3. Add constraints: "8 weeks", "$50k budget"
4. Click "Generate Feature Plan"

### 3. Test Export Functionality

After generating a plan:
1. Click "Export as Markdown"
2. Verify the downloaded file contains the plan details

### 4. Test Recent Plans

1. Generate a plan
2. Go back to form
3. Check the "Recent Plans" section
4. Click on a recent plan to view it

## Troubleshooting

### Backend Issues

**"OPENAI_API_KEY not set"**
- Check that .env file exists in root directory
- Verify OPENAI_API_KEY=sk-... is correctly set
- Restart the backend server

**"Database connection error"**
- Ensure write permissions in the project directory
- Delete tasks_generator.db and restart (it will recreate)
- On Linux/Mac: check file permissions

**"Port 8000 already in use"**
- Find the process using the port
- Windows: `netstat -ano | findstr :8000`
- Mac/Linux: `lsof -i :8000`
- Kill the process or use a different port

### Frontend Issues

**"Cannot connect to API"**
- Ensure backend is running on port 8000
- Check VITE_API_BASE_URL in frontend/.env
- Check browser console for CORS errors
- Verify ALLOWED_ORIGINS in backend .env includes frontend URL

**"npm install fails"**
- Delete node_modules and package-lock.json
- Clear npm cache: `npm cache clean --force`
- Run `npm install` again

### Docker Issues

**"Docker daemon not running"**
- Start Docker Desktop application
- On Linux: `sudo systemctl start docker`

**"Build fails"**
- Ensure .env file exists in root directory
- Check Docker disk space: `docker system df`
- Try rebuilding: `docker-compose build --no-cache`

## Development Workflow

### File Structure While Developing

```
Task_Generators/
├── backend/
│   └── app/
│       ├── routes/         ← Edit endpoints here
│       ├── services/       ← Edit business logic here
│       └── utils/          ← Edit helpers here
├── frontend/
│   └── src/
│       ├── components/     ← Edit React components here
│       ├── pages/          ← Edit pages here
│       └── services/       ← Edit API client here
└── .env                    ← Keep API keys here (don't commit)
```

### Making Changes

**Backend:**
- Edit files in `backend/app/`
- Server auto-reloads with `--reload` flag
- Check backend logs for errors

**Frontend:**
- Edit files in `frontend/src/`
- Browser hot-reloads automatically
- Check browser console for errors

## Production Deployment

### Building for Production

```bash
# Backend
cd backend
pip install -r requirements.txt
# Ensure .env is configured

# Frontend
cd frontend
npm run build
# Creates optimized dist/ folder
```

### Docker Production Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Or with detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Performance Tips

1. **Backend**: Enable caching for LLM responses
2. **Frontend**: Implement React.memo for components
3. **Database**: Add indexes for frequently queried fields
4. **General**: Use Docker for consistent performance across environments

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **OpenAI API**: https://platform.openai.com/docs/
- **Docker**: https://docs.docker.com/

## Next Steps

1. Run the application using one of the methods above
2. Generate a few feature plans to test functionality
3. Check API documentation at http://localhost:8000/docs
4. Customize the LLM prompts in `backend/app/utils/llm.py`
5. Add more categories to engineering tasks
6. Implement additional features as needed

Enjoy building! 🚀
