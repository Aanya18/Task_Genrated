import React, { useState } from 'react';
import './PlanView.css';

export default function PlanView({ plan, onExport, onUpdate }) {
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [tasks, setTasks] = useState(plan.engineering_tasks);

  const handleTaskReorder = (category, fromIndex, toIndex) => {
    const newTasks = { ...tasks };
    const categoryTasks = [...newTasks[category]];
    const [task] = categoryTasks.splice(fromIndex, 1);
    categoryTasks.splice(toIndex, 0, task);
    newTasks[category] = categoryTasks;
    setTasks(newTasks);
  };

  const handleTaskEdit = (category, index, updatedTask) => {
    const newTasks = { ...tasks };
    newTasks[category][index] = updatedTask;
    setTasks(newTasks);
    setEditingTaskId(null);
  };

  const handleSave = () => {
    onUpdate(tasks);
  };

  const handleExport = () => {
    onExport(plan.id);
  };

  return (
    <div className="plan-view">
      <div className="plan-header">
        <h2>Feature Plan</h2>
        <div className="header-actions">
          <button onClick={handleSave} className="btn-primary">
            Save Changes
          </button>
          <button onClick={handleExport} className="btn-secondary">
            Export as Markdown
          </button>
        </div>
      </div>

      <div className="goal-section">
        <h3>Goal</h3>
        <p>{plan.goal}</p>
      </div>

      <div className="user-stories-section">
        <h3>User Stories</h3>
        {plan.user_stories.map((story, index) => (
          <div key={index} className="story-card">
            <h4>{story.title}</h4>
            <p>{story.description}</p>
            <div className="criteria">
              <strong>Acceptance Criteria:</strong>
              <ul>
                {story.acceptance_criteria.map((criterion, i) => (
                  <li key={i}>{criterion}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <div className="tasks-section">
        <h3>Engineering Tasks</h3>
        {Object.entries(tasks).map(([category, categoryTasks]) => (
          <div key={category} className="task-category">
            <h4>{category}</h4>
            {categoryTasks.length === 0 ? (
              <p className="no-tasks">No tasks in this category</p>
            ) : (
              <div className="tasks-list">
                {categoryTasks.map((task, index) => (
                  <div
                    key={index}
                    className={`task-card priority-${task.priority.toLowerCase()}`}
                  >
                    <div className="task-header">
                      <span className="priority-badge">{task.priority}</span>
                      <h5>{task.title}</h5>
                      <span className="effort">{task.estimated_effort}</span>
                    </div>
                    <p className="description">{task.description}</p>
                    <div className="task-actions">
                      {index > 0 && (
                        <button
                          onClick={() =>
                            handleTaskReorder(category, index, index - 1)
                          }
                          className="btn-small"
                        >
                          ↑ Move Up
                        </button>
                      )}
                      {index < categoryTasks.length - 1 && (
                        <button
                          onClick={() =>
                            handleTaskReorder(category, index, index + 1)
                          }
                          className="btn-small"
                        >
                          ↓ Move Down
                        </button>
                      )}
                      <button
                        onClick={() =>
                          setEditingTaskId(`${category}-${index}`)
                        }
                        className="btn-small"
                      >
                        Edit
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="risks-section">
        <h3>Risks & Mitigations</h3>
        {plan.risks.map((risk, index) => (
          <div key={index} className="risk-card">
            <h5>{risk.risk}</h5>
            <div className="risk-details">
              <p>
                <strong>Mitigation:</strong> {risk.mitigation}
              </p>
              <p>
                <strong>Severity:</strong>{' '}
                <span className={`severity-${risk.severity.toLowerCase()}`}>
                  {risk.severity}
                </span>
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="metadata">
        <small>Created: {new Date(plan.created_at).toLocaleString()}</small>
      </div>
    </div>
  );
}
