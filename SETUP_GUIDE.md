# Setup Guide

This guide will help you set up and run the Street Light Fault Detection and Road Accident Alert System.

## Prerequisites

Before starting, ensure you have:
- **Python 3.8 or higher**: [Download](https://www.python.org/downloads/)
- **Node.js 14+ and npm**: [Download](https://nodejs.org/)
- **Git**: [Download](https://git-scm.com/)

## Step 1: Clone/Open the Project

```bash
# If you haven't cloned yet:
git clone <repository-url>
cd street-light-fault-detection-and-road-accident-alert
```

## Step 2: Automated Setup (Recommended)

### Windows Users
```powershell
# Open PowerShell in the project directory and run:
.\startup.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then run startup.ps1 again
```

### macOS/Linux Users
```bash
# Make script executable and run:
chmod +x startup.sh
./startup.sh
```

## Step 3: Manual Setup (If Automated Fails)

### 3.1 Setup Python Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.2 Initialize Database

```bash
cd backend

# Copy environment config
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Initialize database
python database.py

cd ..
```

### 3.3 Start Backend Server

```bash
cd backend
python ws_server.py
```

**Output should show:**
```
✓ Database initialized successfully
✓ WebSocket server running on ws://localhost:8765
```

**Keep this terminal running!**

### 3.4 Setup Frontend (New Terminal)

```bash
cd frontend

# Copy environment config
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Install dependencies
npm install

# Start development server
npm start
```

**Application should open at http://localhost:3000**

## Step 4: Testing the Application

### Register a New User
1. Click "Sign Up"
2. Enter email, phone, and password (min 6 chars)
3. Click "Register"

### Login
1. Use the credentials from registration
2. You should be redirected to the Dashboard

### Test Features
- **Accident Detection**: View detected accidents
- **Light Fault Detection**: View detected light faults
- **Dashboard**: Overview of all alerts

## Step 5: Environment Configuration

### Frontend Configuration (`frontend/.env`)
```env
REACT_APP_WS_URL=ws://localhost:8765
REACT_APP_ENV=development
```

### Backend Configuration (`backend/.env`)
```env
WS_HOST=localhost
WS_PORT=8765
DATABASE_PATH=users.db
ENVIRONMENT=development
```

## Running ML Models

### Accident Detection
```bash
python accident_detection.py
python motion_detection.py
```

### Human Collapse Detection
```bash
python human_collapse_detection.py
```

### Train CNN Model
```
Requires dataset in:
- dataset/train/  (accident/normal image folders)
- dataset/val/    (accident/normal image folders)

python train_accident_cnn.py
```

## Common Issues & Solutions

### Issue: "WebSocket error. Is the backend running?"
**Solution:**
1. Ensure backend server is running: `python backend/ws_server.py`
2. Check if port 8765 is available
3. Verify `REACT_APP_WS_URL` in `frontend/.env`

### Issue: Database file not found
**Solution:**
```bash
cd backend
python database.py
```

### Issue: Port 3000 already in use (Frontend)
**Solution:**
```powershell
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process -Force

# Or use different port:
# In frontend directory, create .env with:
PORT=3001
```

### Issue: Port 8765 already in use (Backend)
**Solution:**
```python
# Edit backend/ws_server.py, change PORT variable:
PORT = 8766  # or any available port
# Update frontend/.env to match
```

### Issue: "Python not found"
**Solution:**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Issue: "npm: command not found"
**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

## Folder Structure After Setup

```
project-root/
├── venv/                    # Python virtual environment
├── backend/
│   ├── users.db            # SQLite database (created)
│   ├── ws_server.py        # WebSocket server
│   ├── database.py
│   ├── .env                # Configuration (created)
│   └── .env.example
├── frontend/
│   ├── node_modules/       # npm dependencies
│   ├── src/
│   ├── .env                # Configuration (created)
│   ├── .env.example
│   └── package.json
└── requirements.txt
```

## Next Steps

1. **Optimize ML Models**: Train CNN with your dataset
2. **Integrate Cameras**: Connect ESP32 or IP cameras
3. **Add Notifications**: Implement email/SMS alerts
4. **Deploy**: Set up production environment
5. **Mobile App**: Develop React Native version

## Getting Help

For debugging:
1. Check browser console (F12) for frontend errors
2. Check terminal output for backend errors
3. Verify all `.env` files are correct
4. Ensure database is initialized: `users.db` should exist

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [React Documentation](https://react.dev)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose)
- [TensorFlow](https://www.tensorflow.org/guide/)

---

Good luck! 🚀
