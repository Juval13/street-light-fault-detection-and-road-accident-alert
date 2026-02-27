import { useState, useEffect } from 'react';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8765';

export const useAlerts = (alertType) => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const token = localStorage.getItem('sessionToken');

  const fetchAlerts = () => {
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
          token: token,
          alert_type: alertType
        }));
      };

      ws.onmessage = (event) => {
        clearTimeout(timeout);
        try {
          const response = JSON.parse(event.data);
          if (response.status === 'ok') {
            setAlerts(response.alerts || []);
          } else {
            setError(response.message || `Failed to fetch ${alertType} alerts`);
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

  useEffect(() => {
    fetchAlerts();
  }, [alertType]);

  return { alerts, loading, error, fetchAlerts };
};
