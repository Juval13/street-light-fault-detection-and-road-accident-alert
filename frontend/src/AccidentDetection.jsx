import React, { useState, useEffect } from 'react';
import './styles.css';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

export default function AccidentDetection() {
  const [accidents, setAccidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    fetchAccidents();
  }, []);

  const fetchAccidents = () => {
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
          alert_type: 'accident'
        }));
      };

      ws.onmessage = (event) => {
        clearTimeout(timeout);
        try {
          const response = JSON.parse(event.data);
          if (response.status === 'ok') {
            setAccidents(response.alerts || []);
          } else {
            setError(response.message || 'Failed to fetch accidents');
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
          <button onClick={fetchAccidents} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
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
        <button onClick={fetchAccidents} style={{marginTop:'10px', padding:'8px 16px', cursor:'pointer'}}>
          Refresh
        </button>
      </div>
    </div>
  );
}
