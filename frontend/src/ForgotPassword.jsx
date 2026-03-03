import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

const ForgotPassword = ({ onLogin }) => {
  const [method, setMethod] = useState('email');
  const [value, setValue] = useState('');
  const [status, setStatus] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);

  // WebSocket logic
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!value) {
      setStatus('Please enter your ' + method);
      return;
    }
    
    setLoading(true);
    setStatus('Sending request...');
    try {
      const ws = new window.WebSocket(WS_URL);
      const timeout = setTimeout(() => {
        ws.close();
        setStatus('Connection timeout. Is the backend running?');
        setLoading(false);
      }, 5000);
      
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'forgot_password',
          method,
          value
        }));
      };
      
      ws.onmessage = (event) => {
        clearTimeout(timeout);
        const resp = JSON.parse(event.data);
        setStatus(resp.message);
        if (resp.status === 'ok') {
          setOtpSent(true);
        }
        setLoading(false);
        ws.close();
      };
      
      ws.onerror = () => {
        clearTimeout(timeout);
        setStatus('WebSocket error. Is backend running?');
        setLoading(false);
      };
    } catch (err) {
      setLoading(false);
      setStatus('Error: ' + err.message);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    
    if (!otp) {
      setStatus('Please enter the OTP');
      return;
    }
    
    setLoading(true);
    setStatus('Verifying OTP...');
    try {
      const ws = new window.WebSocket(WS_URL);
      const timeout = setTimeout(() => {
        ws.close();
        setStatus('Connection timeout. Is the backend running?');
        setLoading(false);
      }, 5000);
      
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'verify_otp',
          method,
          value,
          otp
        }));
      };
      
      ws.onmessage = (event) => {
        clearTimeout(timeout);
        const resp = JSON.parse(event.data);
        setStatus(resp.message);
        setLoading(false);
        if (resp.status === 'ok' && resp.token) {
          // Save session token and auto-login
          localStorage.setItem('sessionToken', resp.token);
          setStatus('OTP verified! Logging you in...');
          setTimeout(() => {
            if (onLogin) {
              onLogin();
            } else {
              window.location.href = '/dashboard';
            }
          }, 1500);
        } else if (resp.status === 'ok') {
          // Success but no token (shouldn't happen)
          setStatus('OTP verified! Redirecting to login...');
          setTimeout(() => {
            window.location.href = '/login';
          }, 1500);
        }
        ws.close();
      };
      
      ws.onerror = () => {
        clearTimeout(timeout);
        setStatus('WebSocket error. Is backend running?');
        setLoading(false);
      };
    } catch (err) {
      setLoading(false);
      setStatus('Error: ' + err.message);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>Forgot Password</h2>
        {!otpSent ? (
          <form onSubmit={handleSubmit}>
            <div style={{marginBottom:16}}>
              <label>
                <input
                  type="radio"
                  name="method"
                  value="email"
                  checked={method === 'email'}
                  onChange={() => setMethod('email')}
                  disabled={loading}
                /> Email
              </label>
              <label style={{marginLeft:24}}>
                <input
                  type="radio"
                  name="method"
                  value="phone"
                  checked={method === 'phone'}
                  onChange={() => setMethod('phone')}
                  disabled={loading}
                /> Phone Number
              </label>
            </div>
            <input
              className="login-input"
              type={method === 'email' ? 'email' : 'tel'}
              placeholder={method === 'email' ? 'Enter your email' : 'Enter your phone number'}
              value={value}
              onChange={e => setValue(e.target.value)}
              required
              disabled={loading}
              style={{marginBottom:16}}
            />
            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? 'Sending...' : 'Send Request'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleOtpSubmit}>
            <p style={{marginBottom:16, color:'#666', fontSize:'14px'}}>
              We've sent an OTP to your {method}. Please enter it below.
            </p>
            <input
              className="login-input"
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={e => setOtp(e.target.value)}
              required
              disabled={loading}
              style={{marginBottom:16}}
            />
            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
          </form>
        )}
        {status && (
          <div style={{
            marginTop:16, 
            color: status.includes('error') ? '#e74c3c' : '#27ae60', 
            fontWeight:'500'
          }}>
            {status}
          </div>
        )}
        <p style={{marginTop:'20px'}}>
          <Link to="/login" style={{color:'#1976d2', textDecoration:'underline'}}>Back to Login</Link>
        </p>
      </div>
    </div>
  );
}

export default ForgotPassword;
