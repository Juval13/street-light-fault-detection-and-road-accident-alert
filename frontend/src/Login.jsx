import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    const ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
      ws.send(JSON.stringify({
        type: 'login',
        email,
        password
      }));
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.status === 'ok') {
        onLogin();
      } else {
        setError(response.message);
      }
      ws.close();
    };

    ws.onerror = (error) => {
      setError('WebSocket error. Is the backend running?');
      console.error('WebSocket error:', error);
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
          />
          <label htmlFor="password" style={{textAlign:'left', width:'100%', fontWeight:'500', marginBottom:4}}>Password</label>
          <input
            id="password"
            className="login-input"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
          {error && <div className="login-error">{error}</div>}
          <button className="login-btn" type="submit">Login</button>
          <div style={{marginTop:16, display:'flex', justifyContent:'space-between', width:'100%'}}>
            <Link to="/forgot-password" style={{color:'#1976d2', textDecoration:'underline', fontWeight:'500'}}>Forgot Password?</Link>
            <Link to="/register" style={{color:'#1976d2', textDecoration:'underline', fontWeight:'500'}}>Sign Up</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
