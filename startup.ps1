#!/bin/bash
# Startup script for Windows (PowerShell)
# Save as: startup.ps1
# Usage: .\startup.ps1

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Street Light & Accident Detection System" -ForegroundColor Cyan
Write-Host "Startup Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create and activate virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
cd backend
python database.py
cd ..

# Start backend server
Write-Host ""
Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host "Backend running on ws://localhost:8765" -ForegroundColor Green
Write-Host ""

# Start in new window
Start-Process powershell -ArgumentList "cd $PWD; .\venv\Scripts\Activate.ps1; cd backend; python ws_server.py"

# Wait for backend to start
Start-Sleep -Seconds 2

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Node.js not found! Please install Node.js 14+" -ForegroundColor Red
    exit 1
}

# Setup frontend
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install -q
    cd ..
}

# Start frontend
Write-Host ""
Write-Host "Starting frontend server..." -ForegroundColor Green
Write-Host "Frontend running on http://localhost:3000" -ForegroundColor Green
cd frontend
npm start
