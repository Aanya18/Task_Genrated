import React, { useEffect, useState } from 'react';
import { healthAPI } from '../services/api';
import './Health.css';

export default function Health() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const response = await healthAPI.getStatus();
      setHealth(response.data);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealth({
        status: 'unhealthy',
        backend: { status: 'unhealthy' },
        database: { status: 'unhealthy' },
        llm: { status: 'unhealthy' },
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="health-loading">Checking system health...</div>;
  }

  if (!health) {
    return <div className="health-error">Unable to fetch health status</div>;
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'green';
      case 'degraded':
        return 'orange';
      case 'unhealthy':
        return 'red';
      default:
        return 'gray';
    }
  };

  return (
    <div className={`health-status status-${getStatusColor(health.status)}`}>
      <h4>System Health: {health.status.toUpperCase()}</h4>
      <div className="health-indicators">
        <div className={`indicator status-${getStatusColor(health.backend.status)}`}>
          <span className="dot"></span>
          <span>Backend</span>
        </div>
        <div className={`indicator status-${getStatusColor(health.database.status)}`}>
          <span className="dot"></span>
          <span>Database</span>
        </div>
        <div className={`indicator status-${getStatusColor(health.llm.status)}`}>
          <span className="dot"></span>
          <span>LLM</span>
        </div>
      </div>
      <small>
        Last updated: {new Date(health.timestamp).toLocaleTimeString()}
      </small>
    </div>
  );
}
