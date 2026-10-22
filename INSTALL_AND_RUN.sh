#!/bin/bash

# FlakeGuard AI - Installation and Run Script
# =============================================

echo "🚀 FlakeGuard AI - Installation and Run Script"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Backend Setup
echo "📦 Step 1: Setting up Backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
echo "Installing Python dependencies (this may take a few minutes)..."
source venv/bin/activate
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Backend dependencies installed"

# Initialize database
echo "Initializing database..."
python -c "from app.core.database import init_db; init_db(); print('✅ Database initialized')"

# Go back to root
cd ..

# Frontend Setup
echo ""
echo "📦 Step 2: Setting up Frontend..."
cd frontend

echo "Installing npm dependencies (this may take a few minutes)..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install npm dependencies"
    exit 1
fi

echo "✅ Frontend dependencies installed"

# Go back to root
cd ..

# Success message
echo ""
echo "✅ Installation Complete!"
echo "========================"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
