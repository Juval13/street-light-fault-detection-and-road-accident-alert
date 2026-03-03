import React, { useEffect, useRef } from 'react';
import { useAlerts } from './useAlerts';
import './styles.css';

export default function LightFaultDetection() {
  const { alerts: faults, loading, error, fetchAlerts } = useAlerts('light_fault');
  const refreshIntervalRef = useRef(null);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    refreshIntervalRef.current = setInterval(() => {
      fetchAlerts();
    }, 5000);

    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, [fetchAlerts]);

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
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
          <h2 style={{margin: 0}}>Light Fault Detection</h2>
          <div style={{fontSize: '14px', color: '#666'}}>
            🔄 Auto-refreshing every 5s
          </div>
        </div>
        {faults.length === 0 ? (
          <p>No light faults detected yet. System is monitoring...</p>
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
        <div style={{marginTop: '20px', display: 'flex', gap: '10px', alignItems: 'center'}}>
          <button onClick={fetchAlerts} style={{padding:'8px 16px', cursor:'pointer', background:'#1976d2', color:'white', border:'none', borderRadius:'4px'}}>
            Refresh Now
          </button>
          <span style={{fontSize: '14px', color: '#666'}}>
            Last updated: {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  );
}
