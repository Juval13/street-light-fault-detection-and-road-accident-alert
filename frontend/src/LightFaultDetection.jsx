import React from 'react';
import { useAlerts } from './useAlerts';
import './styles.css';

export default function LightFaultDetection() {
  const { alerts: faults, loading, error, fetchAlerts } = useAlerts('light_fault');

  if (loading) {
    return (
      <div className="light-fault-detection-container">
        <div className="light-fault-detection-card">
          <h2>Light Fault Detection</h2>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="light-fault-detection-container">
        <div className="light-fault-detection-card">
          <h2>Light Fault Detection</h2>
          <p style={{color:'#e74c3c'}}>{error}</p>
          <button onClick={fetchAlerts} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="light-fault-detection-container">
      <div className="light-fault-detection-card">
        <h2>Light Fault Detection</h2>
        {faults.length === 0 ? (
          <p>No light faults detected yet.</p>
        ) : (
          <table className="light-fault-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Fault Type</th>
                <th>Time Detected</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {faults.map((fault, idx) => (
                <tr key={fault.id}>
                  <td>{idx + 1}</td>
                  <td>{fault.description || 'Light fault detected'}</td>
                  <td>{new Date(fault.timestamp).toLocaleString()}</td>
                  <td><span style={{color:'#f39c12', fontWeight:'bold'}}>Reported</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <button onClick={fetchAlerts} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
          Refresh
        </button>
      </div>
    </div>
  );
}
