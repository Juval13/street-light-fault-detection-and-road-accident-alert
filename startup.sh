#!/bin/bash
# Startup script for macOS/Linux
# Save as: startup.sh
# Usage: bash startup.sh

echo "======================================"
echo "Street Light & Accident Detection System"
echo "Startup Script"
echo "======================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Python not found! Please install Python 3.8+"
    exit 1
fi

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Initialize database
echo "Initializing database..."
cd backend
python3 database.py
cd ..

# Start backend server
echo ""
echo "Starting backend server..."
echo "Backend running on ws://localhost:8765"
echo ""

# Start in new terminal window
open -a Terminal "$(pwd)/start_backend.sh" 2>/dev/null || \
gnome-terminal -- bash -c "source venv/bin/activate; cd backend; python3 ws_server.py; exec bash" &

# Wait for backend to start
sleep 2

# Check Node.js
echo "Checking Node.js installation..."
node --version
if [ $? -ne 0 ]; then
    echo "Node.js not found! Please install Node.js 14+"
    exit 1
fi

# Setup frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install -q
    cd ..
fi

# Start frontend
echo ""
echo "Starting frontend server..."
echo "Frontend running on http://localhost:3000"
cd frontend
npm start
