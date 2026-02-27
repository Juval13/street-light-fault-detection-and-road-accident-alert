import React from 'react';
import { useAlerts } from './useAlerts';
import './styles.css';

export default function AccidentDetection() {
  const { alerts: accidents, loading, error, fetchAlerts } = useAlerts('accident');

  if (loading) {
    return (
      <div className="accident-detection-container">
        <div className="accident-detection-card">
          <h2>Accident Detection</h2>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="accident-detection-container">
        <div className="accident-detection-card">
          <h2>Accident Detection</h2>
          <p style={{color:'#e74c3c'}}>{error}</p>
          <button onClick={fetchAlerts} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="accident-detection-container">
      <div className="accident-detection-card">
        <h2>Accident Detection</h2>
        {accidents.length === 0 ? (
          <p>No accidents detected yet.</p>
        ) : (
          <table className="accident-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Details</th>
                <th>Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {accidents.map((accident, idx) => (
                <tr key={accident.id}>
                  <td>{idx + 1}</td>
                  <td>{accident.description || 'Accident detected'}</td>
                  <td>{new Date(accident.timestamp).toLocaleString()}</td>
                  <td><span style={{color:'#e74c3c', fontWeight:'bold'}}>Alert Sent</span></td>
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
