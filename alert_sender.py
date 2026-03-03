"""
Alert Sender Module
Helper for detection scripts to send alerts to the backend WebSocket server
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WS_URL = 'ws://localhost:8765'

# Store session token (you can get this from login or use a system token)
# For demo purposes, we'll create alerts without authentication
# In production, you should authenticate the detection system

def send_alert_sync(alert_type, description, token=None):
    """
    Send alert synchronously (blocks until sent)
    
    Args:
        alert_type: 'accident', 'light_fault', or 'collapse'
        description: Details about the detection
        token: Optional session token (if None, will use system user)
    """
    try:
        asyncio.run(send_alert_async(alert_type, description, token))
        return True
    except Exception as e:
        logger.error(f"Failed to send alert: {str(e)}")
        return False

async def send_alert_async(alert_type, description, token=None):
    """
    Send alert asynchronously to WebSocket backend
    
    Args:
        alert_type: 'accident', 'light_fault', or 'collapse'
        description: Details about the detection
        token: Optional session token
    """
    try:
        async with websockets.connect(WS_URL) as websocket:
            # If no token provided, try to get demo user token
            if not token:
                token = await get_demo_token(websocket)
            
            # Send alert
            message = {
                'type': 'log_alert',
                'token': token,
                'alert_type': alert_type,
                'description': description
            }
            
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            result = json.loads(response)
            
            if result.get('status') == 'ok':
                logger.info(f"✓ Alert sent: {alert_type} - {description}")
                return True
            else:
                logger.warning(f"⚠ Alert failed: {result.get('message')}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Alert error: {str(e)}")
        return False

async def get_demo_token(websocket):
    """
    Create or login to a demo/system user for detection alerts
    """
    # Try to login with system credentials
    # You should create a user first: email=system@local, password=system123
    try:
        login_msg = {
            'type': 'login',
            'email': 'system@local',
            'password': 'system123'
        }
        await websocket.send(json.dumps(login_msg))
        response = await websocket.recv()
        result = json.loads(response)
        
        if result.get('status') == 'ok':
            return result.get('token')
        else:
            logger.warning("System user not found. Please create one with email: system@local, password: system123")
            return None
    except Exception as e:
        logger.error(f"Failed to get token: {str(e)}")
        return None

# Simple usage functions
def send_accident_alert(description="Accident detected by camera", location="", confidence=None):
    """Send an accident detection alert"""
    details = description
    if location:
        details += f" at {location}"
    if confidence:
        details += f" (confidence: {confidence:.2%})"
    
    return send_alert_sync('accident', details)

def send_light_fault_alert(description="Street light fault detected", light_id=""):
    """Send a light fault alert"""
    details = description
    if light_id:
        details += f" - Light ID: {light_id}"
    
    return send_alert_sync('light_fault', details)

def send_collapse_alert(description="Human collapse detected", location=""):
    """Send a human collapse alert"""
    details = description
    if location:
        details += f" at {location}"
    
    return send_alert_sync('collapse', details)


if __name__ == "__main__":
    # Test the alert sender
    print("Testing alert sender...")
    print("Make sure backend is running on ws://localhost:8765")
    print("Create a user with email: system@local, password: system123")
    
    # Test sending an accident alert
    success = send_accident_alert("Test accident detection", location="Camera 1", confidence=0.95)
    if success:
        print("✓ Test alert sent successfully!")
    else:
        print("✗ Failed to send test alert")
