import asyncio
import websockets
import json
import bcrypt
import logging
import secrets
from database import init_db, get_db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = 'localhost'
PORT = 8765

# In-memory session store (for prototype purposes)
# In a production environment, use a persistent store like Redis
sessions = {}

def validate_email(email):
    """Basic email validation"""
    return '@' in email and len(email) > 5

def validate_password(password):
    """Password must be at least 6 characters"""
    return len(password) >= 6

def validate_phone(phone):
    """Phone number validation"""
    return len(phone) >= 10

def get_user_from_token(token):
    """Get user ID from session token"""
    return sessions.get(token)

async def handler(websocket, path):
    db_conn = None
    try:
        db_conn = get_db()
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
                    cursor = db_conn.cursor()
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    
                    cursor.execute(
                        "INSERT INTO users (email, phone, password) VALUES (?, ?, ?)",
                        (email, phone, hashed_password)
                    )
                    db_conn.commit()
                    
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
                    cursor = db_conn.cursor()
                    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
                    user = cursor.fetchone()
                    
                    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                        token = secrets.token_hex(16)
                        sessions[token] = user['id']
                        response = {'status': 'ok', 'message': 'Login successful', 'token': token}
                        logger.info(f"User logged in: {email}")
                    else:
                        response = {'status': 'error', 'message': 'Invalid credentials'}
                except Exception as e:
                    logger.error(f"Login error: {str(e)}")
                    response = {'status': 'error', 'message': 'Database error'}
                
                await websocket.send(json.dumps(response))
            
            elif request_type == 'logout':
                token = data.get('token')
                if token and token in sessions:
                    del sessions[token]
                    logger.info(f"User logged out with token: {token[:6]}...")
                response = {'status': 'ok', 'message': 'Logged out'}
                await websocket.send(json.dumps(response))

            elif request_type == 'forgot_password':
                # This endpoint does not need to be authenticated
                # ... (code remains the same)
                pass
            
            elif request_type == 'log_alert':
                token = data.get('token')
                user_id = get_user_from_token(token)
                
                if not user_id:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Authentication failed'}))
                    continue

                alert_type = data.get('alert_type', '').strip()
                description = data.get('description', '').strip()
                
                if alert_type not in ['accident', 'light_fault', 'collapse']:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Invalid alert data'}))
                    continue
                
                try:
                    cursor = db_conn.cursor()
                    cursor.execute(
                        "INSERT INTO alerts (user_id, alert_type, description) VALUES (?, ?, ?)",
                        (user_id, alert_type, description)
                    )
                    db_conn.commit()
                    
                    response = {'status': 'ok', 'message': 'Alert logged'}
                    logger.info(f"Alert logged: type={alert_type}, user={user_id}")
                except Exception as e:
                    logger.error(f"Alert logging error: {str(e)}")
                    response = {'status': 'error', 'message': 'Failed to log alert'}
                
                await websocket.send(json.dumps(response))
            
            elif request_type == 'get_alerts':
                token = data.get('token')
                user_id = get_user_from_token(token)

                if not user_id:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Authentication failed'}))
                    continue

                alert_type = data.get('alert_type')
                
                try:
                    cursor = db_conn.cursor()
                    
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
                    
                    alerts = []
                    for row in rows:
                        alerts.append({
                            'id': row['id'],
                            'alert_type': row['alert_type'],
                            'description': row['description'],
                            'timestamp': row['timestamp']
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
    finally:
        if db_conn:
            db_conn.close()

async def main():
    """Initialize database and start WebSocket server"""
    init_db()
    async with websockets.serve(handler, HOST, PORT):
        logger.info(f'✓ WebSocket server running on ws://{HOST}:{PORT}')
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
