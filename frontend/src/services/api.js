import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const featureAPI = {
  // Generate a new feature plan
  generatePlan: (goal, users, constraints) =>
    apiClient.post('/features/generate', {
      goal,
      users,
      constraints,
    }),

  // Get recent feature plans
  getRecentPlans: (limit = 5) =>
    apiClient.get('/features/recent', { params: { limit } }),

  // Get a specific feature plan
  getPlan: (planId) =>
    apiClient.get(`/features/${planId}`),

  // Update engineering tasks
  updateTasks: (planId, engineeringTasks) =>
    apiClient.put(`/features/${planId}/tasks`, {
      engineering_tasks: engineeringTasks,
    }),

  // Export as markdown
  exportMarkdown: (planId) =>
    apiClient.get(`/features/${planId}/export`),
};

export const healthAPI = {
  // Get system health status
  getStatus: () =>
    apiClient.get('/health/status'),

  // Ping endpoint
  ping: () =>
    apiClient.get('/health/ping'),
};

export default apiClient;
