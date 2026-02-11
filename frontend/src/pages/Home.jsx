import React, { useState } from 'react';
import FeatureForm from '../components/FeatureForm';
import PlanView from '../components/PlanView';
import RecentPlans from '../components/RecentPlans';
import Health from '../components/Health';
import { featureAPI } from '../services/api';
import './Home.css';

export default function Home() {
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [shouldRefreshRecent, setShouldRefreshRecent] = useState(false);

  const handleGeneratePlan = async (data) => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');

      const response = await featureAPI.generatePlan(
        data.goal,
        data.users,
        data.constraints
      );

      setCurrentPlan(response.data);
      setSuccess('Feature plan generated successfully!');
      setShouldRefreshRecent(true);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      console.error('Error generating plan:', error);
      setError(
        error.response?.data?.detail ||
          'Failed to generate feature plan. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId) => {
    try {
      setLoading(true);
      setError('');
      const response = await featureAPI.getPlan(planId);
      setCurrentPlan(response.data);
    } catch (error) {
      console.error('Error fetching plan:', error);
      setError('Failed to load feature plan');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTasks = async (tasks) => {
    try {
      setLoading(true);
      setError('');
      await featureAPI.updateTasks(currentPlan.id, tasks);
      setSuccess('Tasks updated successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      console.error('Error updating tasks:', error);
      setError('Failed to update tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleExportMarkdown = async (planId) => {
    try {
      setLoading(true);
      const response = await featureAPI.exportMarkdown(planId);
      const element = document.createElement('a');
      element.setAttribute(
        'href',
        'data:text/markdown;charset=utf-8,' +
          encodeURIComponent(response.data.content)
      );
      element.setAttribute('download', response.data.filename);
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      setSuccess('Feature plan exported successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      console.error('Error exporting plan:', error);
      setError('Failed to export feature plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <header className="app-header">
        <div className="header-content">
          <h1>📋 Tasks Generator</h1>
          <p>Generate comprehensive feature plans powered by AI</p>
        </div>
        <Health />
      </header>

      <main className="app-main">
        {error && (
          <div className="alert alert-error">
            <strong>Error:</strong> {error}
          </div>
        )}
        {success && (
          <div className="alert alert-success">
            <strong>Success:</strong> {success}
          </div>
        )}

        {!currentPlan ? (
          <>
            <FeatureForm onSubmit={handleGeneratePlan} isLoading={loading} />
            <RecentPlans onSelectPlan={handleSelectPlan} />
          </>
        ) : (
          <>
            <button
              onClick={() => setCurrentPlan(null)}
              className="btn-back"
            >
              ← Back to Form
            </button>
            <PlanView
              plan={currentPlan}
              onUpdate={handleUpdateTasks}
              onExport={handleExportMarkdown}
            />
          </>
        )}
      </main>

      <footer className="app-footer">
        <p>Tasks Generator © 2024 | Powered by FastAPI & OpenAI</p>
      </footer>
    </div>
  );
}
