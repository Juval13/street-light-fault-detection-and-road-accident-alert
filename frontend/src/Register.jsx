import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './styles.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

const Register = () => {
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [status, setStatus] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        setStatus('');
        
        // Validation
        if (!email || !phone || !password) {
            setStatus('All fields are required');
            return;
        }
        
        if (password !== confirmPassword) {
            setStatus('Passwords do not match');
            return;
        }
        
        if (password.length < 6) {
            setStatus('Password must be at least 6 characters long');
            return;
        }
        
        if (!/^\d{10,}$/.test(phone.replace(/\D/g, ''))) {
            setStatus('Please enter a valid phone number');
            return;
        }
        
        setLoading(true);
        setStatus('Registering...');
        const ws = new WebSocket(WS_URL);
        
        const timeout = setTimeout(() => {
            ws.close();
            setStatus('Connection timeout. Is the backend running?');
            setLoading(false);
        }, 5000);

        ws.onopen = () => {
            ws.send(JSON.stringify({
                type: 'register',
                email,
                phone,
                password
            }));
        };

        ws.onmessage = (event) => {
            clearTimeout(timeout);
            const response = JSON.parse(event.data);
            setStatus(response.message);
            if (response.status === 'ok') {
                setLoading(false);
                setTimeout(() => {
                    navigate('/login');
                }, 2000);
            } else {
                setLoading(false);
            }
            ws.close();
        };

        ws.onerror = (error) => {
            clearTimeout(timeout);
            setStatus('WebSocket error. Is the backend running?');
            console.error('WebSocket error:', error);
            setLoading(false);
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
                        disabled={loading}
                    />
                    <input
                        className="login-input"
                        type="tel"
                        placeholder="Phone Number"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        required
                        disabled={loading}
                    />
                    <input
                        className="login-input"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                    />
                    <input
                        className="login-input"
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        disabled={loading}
                    />
                    <button className="login-btn" type="submit" disabled={loading}>
                        {loading ? 'Registering...' : 'Register'}
                    </button>
                </form>
                {status && <p style={{ color: status.includes('error') || status.includes('does not') ? '#e74c3c' : '#27ae60' }}>{status}</p>}
                <p>
                    Already have an account? <Link to="/login">Login here</Link>
                </p>
            </div>
        </div>
    );
};

export default Register;