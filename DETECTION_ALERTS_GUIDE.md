# Real-Time Detection Alert System - Setup Guide

## Overview
Your detection scripts (accident detection, light fault detection) can now automatically send alerts to the website, which will display them in real-time!

## How It Works

1. **Detection Scripts** (Python) → Detect accidents/faults
2. **Alert Sender** (alert_sender.py) → Sends data to backend
3. **Backend Server** (ws_server.py) → Stores alerts in database
4. **Website** (React) → Displays alerts in real-time (auto-refreshes every 5 seconds)

## Setup Steps

### Step 1: Create System User Account

First, create a system user account that the detection scripts will use to send alerts:

1. Open your website: http://localhost:3000
2. Click "Register"
3. Create an account with:
   - **Email**: `system@local`
   - **Password**: `system123`
   - **Phone**: `1234567890`

This account will be used by the Python detection scripts to authenticate and send alerts.

### Step 2: Test the Alert Sender

```bash
# Make sure backend is running
python backend/ws_server.py

# In another terminal, test the alert sender
python alert_sender.py
```

You should see: `✓ Test alert sent successfully!`

### Step 3: Integrate with Your Detection Scripts

#### For Accident Detection:

```python
# Add this to your accident detection script
from alert_sender import send_accident_alert

# When you detect an accident:
if accident_detected:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    description = f"Accident detected at {timestamp}"
    send_accident_alert(description, location="Camera 1", confidence=0.95)
```

#### For Light Fault Detection:

```python
# Add this to your light fault detection script
from alert_sender import send_light_fault_alert

# When you detect a fault:
if light_fault_detected:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    description = f"Light fault detected at {timestamp}"
    send_light_fault_alert(description, light_id="Light-001")
```

### Step 4: Run Detection Scripts with Alerts

I've created example files for you:

**Accident Detection with Alerts:**
```bash
python accident_detection_with_alerts.py
```

**Light Fault Detection with Alerts:**
```bash
python light_fault_detection_with_alerts.py
```

### Step 5: View Alerts on Website

1. Go to http://localhost:3000
2. Login with your user account
3. Navigate to:
   - **Accident Detection** page - shows all accident alerts
   - **Light Fault Detection** page - shows all light fault alerts

The pages auto-refresh every 5 seconds to show new detections!

## Integration with Your Existing Detection Scripts

### For `live_camera_hybrid_accident.py`:

Add at the top:
```python
from alert_sender import send_accident_alert
```

Find where it detects an accident (around where `alert_active` becomes True), and add:
```python
if alert_active and alert_type == "ACCIDENT":
    # Send alert to backend
    description = f"Accident detected with {confidence:.2%} confidence"
    send_accident_alert(description, location="Camera 1", confidence=confidence)
```

Add cooldown logic to avoid duplicate alerts:
```python
last_alert_time = 0
ALERT_COOLDOWN = 30  # seconds

# In detection logic:
current_time = time.time()
if alert_active and (current_time - last_alert_time) > ALERT_COOLDOWN:
    send_accident_alert(...)
    last_alert_time = current_time
```

## Features

✅ **Real-time Alerts**: Detections appear on the website within 5 seconds
✅ **Auto-refresh**: Website pages refresh automatically
✅ **Alert History**: All alerts are stored in the database
✅ **Multiple Alert Types**: Accident, Light Fault, and Human Collapse
✅ **Timestamp Tracking**: Every alert has a timestamp
✅ **No Duplicates**: Cooldown prevents spam alerts

## Troubleshooting

### "Failed to send alert"
- Make sure backend is running: `python backend/ws_server.py`
- Check that system user exists: email=system@local, password=system123

### "Alert Failed - Check Backend"
- Backend might not be running
- System user might not be logged in correctly

### Alerts not showing on website
- Make sure you're logged in
- Check browser console for errors
- Verify backend is running on port 8765

## File Structure

```
├── alert_sender.py                          # Helper module for sending alerts
├── accident_detection_with_alerts.py        # Example: Accident detection
├── light_fault_detection_with_alerts.py     # Example: Light fault detection
├── backend/
│   └── ws_server.py                         # Backend server (handles alerts)
└── frontend/src/
    ├── AccidentDetection.jsx                # Shows accident alerts
    └── LightFaultDetection.jsx              # Shows light fault alerts
```

## Next Steps

1. Integrate `alert_sender.py` into your friend's detection scripts
2. Add location/camera IDs to make alerts more specific
3. Test with real camera feeds
4. Monitor the website to see live alerts

## Demo Flow

1. **Start Backend**: `python backend/ws_server.py`
2. **Start Frontend**: `cd frontend && npm start`
3. **Run Detection**: `python accident_detection_with_alerts.py`
4. **Trigger Detection**: Move something in front of camera suddenly, then stop
5. **Check Website**: Go to Accident Detection page - alert appears!

Enjoy your real-time detection alert system! 🚗💡🚨
