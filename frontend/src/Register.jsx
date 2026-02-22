import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './styles.css';

const Register = () => {
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [status, setStatus] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        setStatus('Registering...');
        const ws = new WebSocket('ws://localhost:8765');

        ws.onopen = () => {
            ws.send(JSON.stringify({
                type: 'register',
                email,
                phone,
                password
            }));
        };

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);
            setStatus(response.message);
            if (response.status === 'ok') {
                setTimeout(() => {
                    navigate('/login');
                }, 2000);
            }
            ws.close();
        };

        ws.onerror = (error) => {
            setStatus('WebSocket error. Is the backend running?');
            console.error('WebSocket error:', error);
            ws.close();
        };
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        className="login-input"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        className="login-input"
                        type="tel"
                        placeholder="Phone Number"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        required
                    />
                    <input
                        className="login-input"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button className="login-btn" type="submit">Register</button>
                </form>
                {status && <p>{status}</p>}
                <p>
                    Already have an account? <Link to="/login">Login here</Link>
                </p>
            </div>
        </div>
    );
};

export default Register;
