import asyncio
import websockets
import json
import sqlite3
import bcrypt

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        db = get_db()
        cursor = db.cursor()

        if data.get('type') == 'register':
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password').encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            
            try:
                cursor.execute("INSERT INTO users (email, phone, password) VALUES (?, ?, ?)", (email, phone, hashed_password))
                db.commit()
                response = {'status': 'ok', 'message': 'Registration successful'}
            except sqlite3.IntegrityError:
                response = {'status': 'error', 'message': 'Email or phone already exists'}
            finally:
                db.close()

            await websocket.send(json.dumps(response))

        elif data.get('type') == 'login':
            email = data.get('email')
            password = data.get('password').encode('utf-8')
            
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            db.close()

            if user and bcrypt.checkpw(password, user[0]):
                response = {'status': 'ok', 'message': 'Login successful'}
            else:
                response = {'status': 'error', 'message': 'Invalid credentials'}
            
            await websocket.send(json.dumps(response))

        elif data.get('type') == 'forgot_password':
            method = data.get('method')
            value = data.get('value')
            
            if method == 'email':
                cursor.execute("SELECT email FROM users WHERE email = ?", (value,))
            else:
                cursor.execute("SELECT phone FROM users WHERE phone = ?", (value,))
            
            user = cursor.fetchone()
            db.close()

            if user:
                # Here you would check user and send email/SMS with OTP
                response = {
                    'status': 'ok',
                    'message': f'Request received for {method}: {value}. If a user exists with this {method}, an OTP will be sent.'
                }
            else:
                response = {
                    'status': 'error',
                    'message': f'No user found with this {method}.'
                }

            await websocket.send(json.dumps(response))
        else:
            await websocket.send(json.dumps({'status': 'error', 'message': 'Unknown request'}))

start_server = websockets.serve(handler, 'localhost', 8765)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_server)
    print('WebSocket server running on ws://localhost:8765')
    asyncio.get_event_loop().run_forever()
