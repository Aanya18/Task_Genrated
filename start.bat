@echo off
REM Quick Start Script for Tasks Generator (Windows)

setlocal enabledelayedexpansion

echo 🚀 Tasks Generator - Quick Start
echo ==================================

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo 📋 Creating .env from template...
    copy .env.example .env
    echo ✅ .env file created. Please update it with your OpenAI API key:
    echo    OPENAI_API_KEY=sk-your-api-key-here
    pause
    exit /b 1
)

echo ✅ .env file configured
echo.

REM Ask user for deployment method
echo How would you like to run the application?
echo 1) Docker Compose (recommended)
echo 2) Local Development
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo 🐳 Starting with Docker Compose...
    echo.
    docker-compose up --build
) else if "%choice%"=="2" (
    echo.
    echo 🏃 Starting Local Development...
    echo.
    
    REM Check Python
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is required but not installed
        pause
        exit /b 1
    )
    
    REM Check Node
    node --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Node.js is required but not installed
        pause
        exit /b 1
    )
    
    REM Backend
    echo 📦 Setting up Backend...
    cd backend
    
    if not exist "venv" (
        python -m venv venv
        call venv\Scripts\activate.bat
        pip install -r requirements.txt
    ) else (
        call venv\Scripts\activate.bat
    )
    
    echo 🚀 Starting Backend on http://localhost:8000
    echo 📚 API Docs available at http://localhost:8000/docs
    start cmd /k "python -m uvicorn app.main:app --reload --port 8000"
    
    cd ..
    
    REM Frontend
    echo.
    echo 📦 Setting up Frontend...
    cd frontend
    
    if not exist "node_modules" (
        call npm install
    )
    
    echo 🚀 Starting Frontend on http://localhost:5173
    start cmd /k "npm run dev"
    
    cd ..
    
    echo.
    echo ✅ Application is running!
    echo    Backend:  http://localhost:8000
    echo    Frontend: http://localhost:5173
    echo.
    echo Keep these windows open to run the application
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)
