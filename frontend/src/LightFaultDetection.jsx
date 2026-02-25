import React, { useState, useEffect } from 'react';
import './styles.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

export default function LightFaultDetection() {
  const [faults, setFaults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    fetchFaults();
  }, []);

  const fetchFaults = () => {
    setLoading(true);
    setError('');
    
    try {
      const ws = new WebSocket(WS_URL);
      const timeout = setTimeout(() => {
        ws.close();
        setError('Connection timeout. Is the backend running?');
        setLoading(false);
      }, 5000);

      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: 'get_alerts',
          user_id: userId,
          alert_type: 'light_fault'
        }));
      };

      ws.onmessage = (event) => {
        clearTimeout(timeout);
        try {
          const response = JSON.parse(event.data);
          if (response.status === 'ok') {
            setFaults(response.alerts || []);
          } else {
            setError(response.message || 'Failed to fetch faults');
          }
        } catch (e) {
          setError('Invalid response format');
        }
        setLoading(false);
        ws.close();
      };

      ws.onerror = () => {
        clearTimeout(timeout);
        setError('WebSocket error. Is the backend running?');
        setLoading(false);
      };
    } catch (err) {
      setError('Error: ' + err.message);
      setLoading(false);
    }
  };

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
          <button onClick={fetchFaults} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
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
        <button onClick={fetchFaults} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
          Refresh
        </button>
      </div>
    </div>
  );
}
