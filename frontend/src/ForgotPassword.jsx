import React, { useState } from 'react';
import './styles.css';

const ForgotPassword = () => {
  const [method, setMethod] = useState('email');
  const [value, setValue] = useState('');
  const [status, setStatus] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState('');

  // WebSocket logic
  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Sending request...');
    try {
      const ws = new window.WebSocket('ws://localhost:8765');
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'forgot_password',
          method,
          value
        }));
      };
      ws.onmessage = (event) => {
        const resp = JSON.parse(event.data);
        setStatus(resp.message);
        if (method === 'email') setOtpSent(true);
        ws.close();
      };
      ws.onerror = () => {
        setStatus('WebSocket error. Is backend running?');
      };
    } catch (err) {
      setStatus('Error: ' + err.message);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    setStatus('Verifying OTP...');
    try {
      const ws = new window.WebSocket('ws://localhost:8765');
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'verify_otp',
          method,
          value,
          otp
        }));
      };
      ws.onmessage = (event) => {
        const resp = JSON.parse(event.data);
        setStatus(resp.message);
        ws.close();
      };
      ws.onerror = () => {
        setStatus('WebSocket error. Is backend running?');
      };
    } catch (err) {
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
                /> Email
              </label>
              <label style={{marginLeft:24}}>
                <input
                  type="radio"
                  name="method"
                  value="phone"
                  checked={method === 'phone'}
                  onChange={() => setMethod('phone')}
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
              style={{marginBottom:16}}
            />
            <button className="login-btn" type="submit">Send Request</button>
          </form>
        ) : (
          <form onSubmit={handleOtpSubmit}>
            <input
              className="login-input"
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={e => setOtp(e.target.value)}
              required
              style={{marginBottom:16}}
            />
            <button className="login-btn" type="submit">Verify OTP</button>
          </form>
        )}
        {status && <div style={{marginTop:16, color:'#1976d2', fontWeight:'500'}}>{status}</div>}
      </div>
    </div>
  );
}

export default ForgotPassword;
