import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!email || !password) {
      setError('Email and password are required');
      setLoading(false);
      return;
    }

    const ws = new WebSocket(WS_URL);
    const timeout = setTimeout(() => {
      ws.close();
      setError('Connection timeout. Is the backend running?');
      setLoading(false);
    }, 5000);

    ws.onopen = () => {
      ws.send(JSON.stringify({
        type: 'login',
        email,
        password
      }));
    };

    ws.onmessage = (event) => {
      clearTimeout(timeout);
      const response = JSON.parse(event.data);
      if (response.status === 'ok') {
        localStorage.setItem('userId', response.user_id);
        localStorage.setItem('userEmail', email);
        onLogin();
      } else {
        setError(response.message || 'Login failed');
      }
      setLoading(false);
      ws.close();
    };

    ws.onerror = (error) => {
      clearTimeout(timeout);
      setError('WebSocket error. Is the backend running?');
      console.error('WebSocket error:', error);
      setLoading(false);
      ws.close();
    };
  };

  return (
    <div className="login-bg-img">
      <div className="shape shape1"></div>
      <div className="shape shape2"></div>
      <div className="shape shape3"></div>
      <div className="login-bg-overlay">
        <form className="login-card" onSubmit={handleSubmit}>
          <h2 className="login-title">Login</h2>
          <label htmlFor="email" style={{textAlign:'left', width:'100%', fontWeight:'500', marginBottom:4}}>Email</label>
          <input
            id="email"
            className="login-input"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            disabled={loading}
          />
          <label htmlFor="password" style={{textAlign:'left', width:'100%', fontWeight:'500', marginBottom:4}}>Password</label>
          <input
            id="password"
            className="login-input"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          {error && <div className="login-error">{error}</div>}
          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
          <div style={{marginTop:16, display:'flex', justifyContent:'space-between', width:'100%'}}>
            <Link to="/forgot-password" style={{color:'#1976d2', textDecoration:'underline', fontWeight:'500'}}>Forgot Password?</Link>
            <Link to="/register" style={{color:'#1976d2', textDecoration:'underline', fontWeight:'500'}}>Sign Up</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
