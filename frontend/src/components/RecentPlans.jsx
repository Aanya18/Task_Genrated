import React, { useEffect, useState } from 'react';
import { featureAPI } from '../services/api';
import './RecentPlans.css';

export default function RecentPlans({ onSelectPlan }) {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      setLoading(true);
      const response = await featureAPI.getRecentPlans(5);
      setPlans(response.data);
      setError('');
    } catch (error) {
      console.error('Error fetching plans:', error);
      setError('Failed to load recent plans');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="recent-plans-loading">Loading recent plans...</div>;
  }

  if (error) {
    return <div className="recent-plans-error">{error}</div>;
  }

  if (plans.length === 0) {
    return (
      <div className="recent-plans-empty">
        No feature plans yet. Generate one to get started!
      </div>
    );
  }

  return (
    <div className="recent-plans">
      <h3>Last 5 Feature Plans</h3>
      <div className="plans-list">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className="plan-item"
            onClick={() => onSelectPlan(plan.id)}
          >
            <div className="plan-info">
              <h4>{plan.goal}</h4>
              <small>
                Created:{' '}
                {new Date(plan.created_at).toLocaleDateString()}{' '}
                {new Date(plan.created_at).toLocaleTimeString()}
              </small>
            </div>
            <span className="plan-id">#{plan.id}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
