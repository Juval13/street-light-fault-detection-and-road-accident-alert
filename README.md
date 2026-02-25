# Street Light Fault Detection & Road Accident Alert System

A comprehensive full-stack application combining computer vision, machine learning, and web technologies to detect road accidents, human collapse/falls, and street light faults with real-time alerts.

## Features

- **Real-time Accident Detection**: Motion detection combined with CNN models
- **Human Collapse Detection**: Pose estimation using MediaPipe
- **Street Light Fault Detection**: Visual detection of faulty street lights
- **User Authentication**: Secure login/registration with password hashing
- **Alert Management**: Log and retrieve detection alerts
- **WebSocket Communication**: Real-time bidirectional communication between frontend and backend
- **Responsive Dashboard**: React-based web interface with role-based access

## Project Structure

```
├── backend/                    # Python WebSocket server
│   ├── ws_server.py           # WebSocket handler
│   ├── database.py            # SQLite database setup
│   └── .env.example           # Backend config template
├── frontend/                  # React application
│   ├── src/
│   │   ├── Login.jsx          # Login component
│   │   ├── Register.jsx       # User registration
│   │   ├── Dashboard.jsx      # Main dashboard
│   │   ├── AccidentDetection.jsx
│   │   ├── LightFaultDetection.jsx
│   │   └── styles.css
│   ├── package.json
│   └── .env.example           # Frontend config template
├── Python ML Models/          # Detection algorithms
│   ├── accident_detection.py
│   ├── motion_detection.py
│   ├── human_collapse_detection.py
│   ├── train_accident_cnn.py
│   └── pose_landmarker_lite.task
└── requirements.txt           # Python dependencies
```

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- OpenCV compatible system

## Quick Start

### 1. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy backend\.env.example backend\.env
# For Unix: cp backend/.env.example backend/.env
```

### 2. Initialize Database

```bash
cd backend
python database.py
# Creates users.db with users and alerts tables
```

### 3. Start Backend Server

```bash
cd backend
python ws_server.py
# Server will run on ws://localhost:8765
```

### 4. Setup & Run Frontend

```bash
cd frontend

# Copy environment config
copy .env.example .env
# For Unix: cp .env.example .env

# Install dependencies
npm install

# Start development server
npm start
# Application opens at http://localhost:3000
```

## Configuration

### Environment Variables

#### Frontend (.env)
```
REACT_APP_WS_URL=ws://localhost:8765
REACT_APP_ENV=development
```

#### Backend (.env)
```
WS_HOST=localhost
WS_PORT=8765
DATABASE_PATH=users.db
ENVIRONMENT=development
```

## Usage

### User Registration
1. Click "Sign Up" on login page
2. Enter email, phone number, and password (min 6 chars)
3. Submit to create account

### User Login
1. Enter registered email and password
2. Access dashboard and detection features

### View Detections
- **Accident Detection**: Real-time accident alerts
- **Light Fault Detection**: Street light faults reported
- **Dashboard**: Overview of all alerts

### Running ML Models

#### Accident Detection (Motion-based)
```bash
python accident_detection.py
python motion_detection.py
```

#### Human Collapse Detection
```bash
python human_collapse_detection.py
```

#### Training CNN Model
```bash
# Requires dataset in dataset/train and dataset/val directories
python train_accident_cnn.py
```

## API Endpoints (WebSocket)

### Authentication
- `type: 'login'` - User login
- `type: 'register'` - User registration
- `type: 'forgot_password'` - Password reset request

### Alerts
- `type: 'log_alert'` - Log detection alert
  ```json
  {
    "type": "log_alert",
    "user_id": 1,
    "alert_type": "accident|light_fault|collapse",
    "description": "Description of the alert"
  }
  ```

- `type: 'get_alerts'` - Retrieve user alerts
  ```json
  {
    "type": "get_alerts",
    "user_id": 1,
    "alert_type": "accident|light_fault|collapse|null"
  }
  ```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Alerts Table
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    alert_type TEXT NOT NULL,
    description TEXT,
    latitude REAL,
    longitude REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

## Security Features

- Password hashing with bcrypt
- SQL parameterized queries (SQL injection prevention)
- Input validation on all endpoints
- WebSocket error handling
- Secure session management with localStorage

## Troubleshooting

### WebSocket Connection Error
- Ensure backend is running: `python backend/ws_server.py`
- Check if port 8765 is not blocked by firewall
- Verify `REACT_APP_WS_URL` in frontend `.env`

### Database Issues
- Delete `users.db` and run `python backend/database.py` again
- Check file permissions in backend directory

### Frontend Port Already in Use
```bash
# Kill process on port 3000 (Windows PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process

# Kill process on port 3000 (Unix)
lsof -ti:3000 | xargs kill -9
```

## Development

### Running Tests
```bash
# Currently no automated tests (to be implemented)
# Manual testing recommended until test suite is added
```

### Code Quality
- Use proper error handling
- Validate all inputs
- Log important events
- Comment complex algorithms

## Future Enhancements

- [ ] Distance-based alert notifications
- [ ] SMS/Email alert integration
- [ ] Real-time map visualization
- [ ] Machine learning model optimization
- [ ] Mobile app (React Native)
- [ ] Unit and integration tests
- [ ] Docker deployment support
- [ ] API rate limiting
- [ ] User preferences and settings
- [ ] Alert history analytics

## License

This project is part of an S6 academic curriculum project.

## Support

For issues or questions, please check:
1. `.env` configuration files are properly set up
2. All dependencies are installed
3. Backend server is running
4. Database is initialized

## Contributors

This is a collaborative S6 project.
