import React from 'react';
import './styles.css';

import { useNavigate } from 'react-router-dom';

export default function Dashboard({ onLogout }) {
  const navigate = useNavigate();
  return (
    <div className="dashboard-bg">
      <div className="dashboard-card">
        <h1 className="dashboard-title">Dashboard</h1>
        <div className="dashboard-options">
          <button className="dashboard-btn" onClick={() => navigate('/accident-detection')}>1. Accident Detection</button>
          <button className="dashboard-btn" onClick={() => navigate('/light-fault-detection')}>2. Light Fault Detection</button>
        </div>
        <button className="logout-btn" onClick={onLogout} style={{marginTop: '20px'}}>
          Logout
        </button>
      </div>
    </div>
  );
}