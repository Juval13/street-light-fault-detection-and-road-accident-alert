import React from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';

import Login from './Login';
import Dashboard from './Dashboard';
import AccidentDetection from './AccidentDetection';
import LightFaultDetection from './LightFaultDetection';
import ForgotPassword from './ForgotPassword';
import Register from './Register';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(!!localStorage.getItem('sessionToken'));
  const navigate = useNavigate();

  const handleLogin = () => {
    setIsAuthenticated(true);
    navigate('/dashboard');
  };

  const handleLogout = () => {
    const token = localStorage.getItem('sessionToken');
    if (token) {
      const ws = new WebSocket(WS_URL);
      ws.onopen = () => {
        ws.send(JSON.stringify({ type: 'logout', token: token }));
        ws.close();
      };
    }
    localStorage.removeItem('sessionToken');
    setIsAuthenticated(false);
    navigate('/login');
  };

  return (
    <div className="app-container">
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login onLogin={handleLogin} /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/accident-detection" element={isAuthenticated ? <AccidentDetection /> : <Navigate to="/login" />} />
        <Route path="/light-fault-detection" element={isAuthenticated ? <LightFaultDetection /> : <Navigate to="/login" />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </div>
  );
}
