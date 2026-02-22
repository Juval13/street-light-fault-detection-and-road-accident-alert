import React from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';

import Login from './Login';
import Dashboard from './Dashboard';
import AccidentDetection from './AccidentDetection';
import LightFaultDetection from './LightFaultDetection';
import ForgotPassword from './ForgotPassword';
import Register from './Register';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    setIsAuthenticated(true);
    navigate('/dashboard');
  };

  return (
    <div className="app-container">
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/accident-detection" element={isAuthenticated ? <AccidentDetection /> : <Navigate to="/login" />} />
        <Route path="/light-fault-detection" element={isAuthenticated ? <LightFaultDetection /> : <Navigate to="/login" />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </div>
  );
}
