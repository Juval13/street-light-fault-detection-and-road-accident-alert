import asyncio
import websockets
import json
import bcrypt
import logging
from database import init_db, get_db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = 'localhost'
PORT = 8765

def validate_email(email):
    """Basic email validation"""
    return '@' in email and len(email) > 5

def validate_password(password):
    """Password must be at least 6 characters"""
    return len(password) >= 6

def validate_phone(phone):
    """Phone number validation"""
    return len(phone) >= 10

async def handler(websocket, path):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid JSON'}))
                continue

            request_type = data.get('type')
            
            if request_type == 'register':
                email = data.get('email', '').strip()
                phone = data.get('phone', '').strip()
                password = data.get('password', '')
                
                # Validation
                if not email or not validate_email(email):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid email format'}))
                    continue
                
                if not phone or not validate_phone(phone):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid phone number'}))
                    continue
                
                if not password or not validate_password(password):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Password must be at least 6 characters'}))
                    continue
                
                try:
                    db = get_db()
                    cursor = db.cursor()
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    cursor.execute(
                        "INSERT INTO users (email, phone, password) VALUES (?, ?, ?)",
                        (email, phone, hashed_password)
                    )
                    db.commit()
                    db.close()
                    
                    response = {'status': 'ok', 'message': 'Registration successful'}
                    logger.info(f"User registered: {email}")
                except Exception as e:
                    logger.error(f"Registration error: {str(e)}")
                    response = {'status': 'error', 'message': 'Email or phone already exists'}
                
                await websocket.send(json.dumps(response))

            elif request_type == 'login':
                email = data.get('email', '').strip()
                password = data.get('password', '')
                
                if not email or not password:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Email and password required'}))
                    continue
                
                try:
                    db = get_db()
                    cursor = db.cursor()
                    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
                    user = cursor.fetchone()
                    db.close()
                    
                    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                        response = {'status': 'ok', 'message': 'Login successful', 'user_id': user[0]}
                        logger.info(f"User logged in: {email}")
                    else:
                        response = {'status': 'error', 'message': 'Invalid credentials'}
                except Exception as e:
                    logger.error(f"Login error: {str(e)}")
                    response = {'status': 'error', 'message': 'Database error'}
                
                await websocket.send(json.dumps(response))

            elif request_type == 'forgot_password':
                method = data.get('method', '').lower()
                value = data.get('value', '').strip()
                
                if method not in ['email', 'phone']:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid method'}))
                    continue
                
                if not value:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Value required'}))
                    continue
                
                try:
                    db = get_db()
                    cursor = db.cursor()
                    
                    if method == 'email':
                        cursor.execute("SELECT id FROM users WHERE email = ?", (value,))
                    else:
                        cursor.execute("SELECT id FROM users WHERE phone = ?", (value,))
                    
                    user = cursor.fetchone()
                    db.close()
                    
                    # Always return success for security (don't reveal if user exists)
                    response = {
                        'status': 'ok',
                        'message': f'If a user exists with this {method}, a reset link will be sent.'
                    }
                    if user:
                        logger.info(f"Password reset requested for {method}: {value}")
                except Exception as e:
                    logger.error(f"Forgot password error: {str(e)}")
                    response = {'status': 'error', 'message': 'Database error'}
                
                await websocket.send(json.dumps(response))
            
            elif request_type == 'log_alert':
                """Log accident/fault detection alert"""
                user_id = data.get('user_id')
                alert_type = data.get('alert_type', '').strip()
                description = data.get('description', '').strip()
                
                if not user_id or alert_type not in ['accident', 'light_fault', 'collapse']:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid alert data'}))
                    continue
                
                try:
                    db = get_db()
                    cursor = db.cursor()
                    cursor.execute(
                        "INSERT INTO alerts (user_id, alert_type, description) VALUES (?, ?, ?)",
                        (user_id, alert_type, description)
                    )
                    db.commit()
                    db.close()
                    
                    response = {'status': 'ok', 'message': 'Alert logged'}
                    logger.info(f"Alert logged: type={alert_type}, user={user_id}")
                except Exception as e:
                    logger.error(f"Alert logging error: {str(e)}")
                    response = {'status': 'error', 'message': 'Failed to log alert'}
                
                await websocket.send(json.dumps(response))
            
            elif request_type == 'get_alerts':
                """Retrieve alerts for user"""
                user_id = data.get('user_id')
                alert_type = data.get('alert_type')
                
                if not user_id:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'User ID required'}))
                    continue
                
                try:
                    db = get_db()
                    cursor = db.cursor()
                    
                    if alert_type:
                        cursor.execute(
                            "SELECT id, alert_type, description, timestamp FROM alerts WHERE user_id = ? AND alert_type = ? ORDER BY timestamp DESC LIMIT 50",
                            (user_id, alert_type)
                        )
                    else:
                        cursor.execute(
                            "SELECT id, alert_type, description, timestamp FROM alerts WHERE user_id = ? ORDER BY timestamp DESC LIMIT 50",
                            (user_id,)
                        )
                    
                    rows = cursor.fetchall()
                    db.close()
                    
                    alerts = []
                    for row in rows:
                        alerts.append({
                            'id': row[0],
                            'alert_type': row[1],
                            'description': row[2],
                            'timestamp': row[3]
                        })
                    
                    response = {
                        'status': 'ok',
                        'alerts': alerts,
                        'count': len(alerts)
                    }
                    logger.info(f"Alerts retrieved for user {user_id}: {len(alerts)} alerts")
                except Exception as e:
                    logger.error(f"Get alerts error: {str(e)}")
                    response = {'status': 'error', 'message': 'Failed to retrieve alerts'}
                
                await websocket.send(json.dumps(response))
            
            else:
                await websocket.send(json.dumps({'status': 'error', 'message': 'Unknown request type'}))
    
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

async def main():
    """Initialize database and start WebSocket server"""
    init_db()
    async with websockets.serve(handler, HOST, PORT):
        logger.info(f'✓ WebSocket server running on ws://{HOST}:{PORT}')
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
