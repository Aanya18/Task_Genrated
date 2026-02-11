#!/bin/bash
# Quick Start Script for Tasks Generator

set -e

echo "🚀 Tasks Generator - Quick Start"
echo "=================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📋 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your OpenAI API key:"
    echo "   OPENAI_API_KEY=sk-your-api-key-here"
    exit 1
fi

# Check for OPENAI_API_KEY
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "❌ OPENAI_API_KEY not properly set in .env"
    exit 1
fi

echo "✅ .env file configured"
echo ""

# Ask user for deployment method
echo "How would you like to run the application?"
echo "1) Docker Compose (recommended)"
echo "2) Local Development"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🐳 Starting with Docker Compose..."
        echo ""
        docker-compose up --build
        ;;
    2)
        echo ""
        echo "🏃 Starting Local Development..."
        echo ""
        
        # Check Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is required but not installed"
            exit 1
        fi
        
        # Check Node
        if ! command -v node &> /dev/null; then
            echo "❌ Node.js is required but not installed"
            exit 1
        fi
        
        # Backend
        echo "📦 Setting up Backend..."
        cd backend
        
        if [ ! -d "venv" ]; then
            python3 -m venv venv
            source venv/bin/activate || . venv/Scripts/activate
            pip install -r requirements.txt
        else
            source venv/bin/activate || . venv/Scripts/activate
        fi
        
        echo "🚀 Starting Backend on http://localhost:8000"
        echo "📚 API Docs available at http://localhost:8000/docs"
        python3 -m uvicorn app.main:app --reload --port 8000 &
        BACKEND_PID=$!
        
        cd ..
        
        # Frontend
        echo ""
        echo "📦 Setting up Frontend..."
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        
        echo "🚀 Starting Frontend on http://localhost:5173"
        npm run dev &
        FRONTEND_PID=$!
        
        cd ..
        
        echo ""
        echo "✅ Application is running!"
        echo "   Backend:  http://localhost:8000"
        echo "   Frontend: http://localhost:5173"
        echo ""
        echo "Press Ctrl+C to stop"
        
        wait
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
