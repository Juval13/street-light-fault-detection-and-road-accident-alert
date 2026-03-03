import asyncio
import websockets
import json
import bcrypt
import logging
import secrets
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from database import init_db, get_db

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = 'localhost'
PORT = 8765

# Email configuration from environment variables
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', SMTP_USER)

# In-memory session store (for prototype purposes)
# In a production environment, use a persistent store like Redis
sessions = {}

# In-memory OTP store: {email: {otp: code, expires: timestamp}}
otps = {}

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

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def store_otp(email, otp):
    """Store OTP with 5 minute expiration"""
    otps[email] = {
        'otp': otp,
        'expires': time.time() + 300  # 5 minutes
    }
    logger.info(f"OTP for {email}: {otp}")  # For development - remove in production

def verify_otp(email, otp):
    """Verify OTP and check expiration"""
    if email not in otps:
        return False
    
    stored = otps[email]
    if time.time() > stored['expires']:
        del otps[email]
        return False
    
    if stored['otp'] == otp:
        del otps[email]  # OTP can only be used once
        return True
    
    return False

def send_otp_email(to_email, otp):
    """Send OTP via email using SMTP"""
    if not EMAIL_ENABLED:
        logger.info(f"Email disabled. OTP for {to_email}: {otp}")
        return True
    
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error("SMTP credentials not configured")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Your OTP Code - Street Light Fault Detection'
        msg['From'] = SMTP_FROM_EMAIL
        msg['To'] = to_email
        
        # Email body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f6fb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #1976d2; text-align: center;">Your OTP Code</h2>
              <p style="font-size: 16px; color: #333;">Hello,</p>
              <p style="font-size: 16px; color: #333;">Your One-Time Password (OTP) for login is:</p>
              <div style="background: #e3f2fd; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                <h1 style="color: #1976d2; font-size: 36px; letter-spacing: 8px; margin: 0;">{otp}</h1>
              </div>
              <p style="font-size: 14px; color: #666;">This OTP is valid for <strong>5 minutes</strong>.</p>
              <p style="font-size: 14px; color: #666;">If you didn't request this OTP, please ignore this email.</p>
              <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
              <p style="font-size: 12px; color: #999; text-align: center;">Street Light Fault Detection & Road Accident Alert System</p>
            </div>
          </body>
        </html>
        """
        
        text = f"Your OTP code is: {otp}\n\nThis OTP is valid for 5 minutes.\n\nIf you didn't request this OTP, please ignore this email."
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"OTP email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
        return False

async def handler(websocket):
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

            elif request_type == 'request_otp':
                email = data.get('email', '').strip()
                
                if not email or not validate_email(email):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Valid email required'}))
                    continue
                
                try:
                    cursor = db_conn.cursor()
                    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                    user = cursor.fetchone()
                    
                    if user:
                        otp = generate_otp()
                        store_otp(email, otp)
                        
                        # Send OTP via email
                        email_sent = send_otp_email(email, otp)
                        
                        if EMAIL_ENABLED:
                            if email_sent:
                                response = {'status': 'ok', 'message': 'OTP sent to your email'}
                            else:
                                response = {'status': 'error', 'message': 'Failed to send email. Please try again.'}
                        else:
                            # Development mode: show OTP in response
                            response = {'status': 'ok', 'message': f'OTP sent! Your OTP is: {otp}', 'otp': otp}
                        
                        logger.info(f"OTP requested for: {email}")
                    else:
                        # Don't reveal if email exists or not (security)
                        response = {'status': 'ok', 'message': 'If email exists, OTP has been sent'}
                except Exception as e:
                    logger.error(f"Request OTP error: {str(e)}")
                    response = {'status': 'error', 'message': 'Error sending OTP'}
                
                await websocket.send(json.dumps(response))
            
            elif request_type == 'verify_otp':
                # Support both formats: {email, otp} and {method, value, otp}
                email = data.get('email', '').strip()
                method = data.get('method', '').strip()
                value = data.get('value', '').strip()
                otp = data.get('otp', '').strip()
                
                # Determine which email to use for OTP verification
                if method and value:
                    # Forgot password flow: method + value format
                    if method == 'email':
                        lookup_email = value
                    else:  # method == 'phone'
                        # Need to get email from phone number
                        try:
                            cursor = db_conn.cursor()
                            cursor.execute("SELECT email FROM users WHERE phone = ?", (value,))
                            phone_user = cursor.fetchone()
                            if phone_user:
                                lookup_email = phone_user['email']
                            else:
                                await websocket.send(json.dumps({'status': 'error', 'message': 'User not found'}))
                                continue
                        except Exception as e:
                            logger.error(f"Phone lookup error: {str(e)}")
                            await websocket.send(json.dumps({'status': 'error', 'message': 'Verification error'}))
                            continue
                elif email:
                    # Direct OTP login flow: email format
                    lookup_email = email
                else:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Email/Phone and OTP required'}))
                    continue
                
                if not otp:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'OTP required'}))
                    continue
                
                try:
                    if verify_otp(lookup_email, otp):
                        cursor = db_conn.cursor()
                        cursor.execute("SELECT id FROM users WHERE email = ?", (lookup_email,))
                        user = cursor.fetchone()
                        
                        if user:
                            token = secrets.token_hex(16)
                            sessions[token] = user['id']
                            response = {'status': 'ok', 'message': 'OTP verified successfully', 'token': token}
                            logger.info(f"User logged in via OTP: {lookup_email}")
                        else:
                            response = {'status': 'error', 'message': 'User not found'}
                    else:
                        response = {'status': 'error', 'message': 'Invalid or expired OTP'}
                except Exception as e:
                    logger.error(f"Verify OTP error: {str(e)}")
                    response = {'status': 'error', 'message': 'Verification error'}
                
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
                method = data.get('method', 'email').strip()
                value = data.get('value', '').strip()
                
                if not value:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Email or phone required'}))
                    continue
                
                if method == 'email' and not validate_email(value):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Valid email required'}))
                    continue
                
                if method == 'phone' and not validate_phone(value):
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Valid phone number required'}))
                    continue
                
                try:
                    cursor = db_conn.cursor()
                    if method == 'email':
                        cursor.execute("SELECT id FROM users WHERE email = ?", (value,))
                    else:
                        cursor.execute("SELECT id, email FROM users WHERE phone = ?", (value,))
                    
                    user = cursor.fetchone()
                    
                    if user:
                        otp = generate_otp()
                        if method == 'email':
                            store_otp(value, otp)
                            email_sent = send_otp_email(value, otp)
                            
                            if EMAIL_ENABLED:
                                if email_sent:
                                    response = {'status': 'ok', 'message': 'Password reset OTP sent to your email'}
                                else:
                                    response = {'status': 'error', 'message': 'Failed to send email. Please try again.'}
                            else:
                                # Development mode: show OTP in response
                                response = {'status': 'ok', 'message': f'OTP sent! Your OTP is: {otp}', 'otp': otp}
                        else:
                            # Phone-based OTP (SMS not implemented yet)
                            # Store OTP using the email associated with the phone
                            user_email = user[1] if len(user) > 1 else None
                            if user_email:
                                store_otp(user_email, otp)
                                response = {'status': 'ok', 'message': f'SMS not configured. Your OTP is: {otp}', 'otp': otp}
                            else:
                                response = {'status': 'error', 'message': 'Unable to send OTP'}
                        
                        logger.info(f"Password reset OTP requested for: {method}={value}")
                    else:
                        # Don't reveal if user exists or not (security)
                        response = {'status': 'ok', 'message': 'If account exists, OTP has been sent'}
                except Exception as e:
                    logger.error(f"Forgot password error: {str(e)}")
                    response = {'status': 'error', 'message': 'Error processing request'}
                
                await websocket.send(json.dumps(response))
            
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
