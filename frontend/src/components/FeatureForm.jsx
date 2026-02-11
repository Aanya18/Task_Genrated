import React, { useState } from 'react';
import './FeatureForm.css';

export default function FeatureForm({ onSubmit, isLoading }) {
  const [goal, setGoal] = useState('');
  const [users, setUsers] = useState(['']);
  const [constraints, setConstraints] = useState(['']);
  const [error, setError] = useState('');

  const handleAddUser = () => {
    setUsers([...users, '']);
  };

  const handleRemoveUser = (index) => {
    if (users.length > 1) {
      setUsers(users.filter((_, i) => i !== index));
    }
  };

  const handleUserChange = (index, value) => {
    const newUsers = [...users];
    newUsers[index] = value;
    setUsers(newUsers);
  };

  const handleAddConstraint = () => {
    setConstraints([...constraints, '']);
  };

  const handleRemoveConstraint = (index) => {
    if (constraints.length > 1) {
      setConstraints(constraints.filter((_, i) => i !== index));
    }
  };

  const handleConstraintChange = (index, value) => {
    const newConstraints = [...constraints];
    newConstraints[index] = value;
    setConstraints(newConstraints);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!goal.trim()) {
      setError('Goal is required');
      return;
    }

    const filteredUsers = users.filter((u) => u.trim());
    if (filteredUsers.length === 0) {
      setError('At least one user persona is required');
      return;
    }

    const filteredConstraints = constraints.filter((c) => c.trim());
    if (filteredConstraints.length === 0) {
      setError('At least one constraint is required');
      return;
    }

    onSubmit({
      goal: goal.trim(),
      users: filteredUsers,
      constraints: filteredConstraints,
    });
  };

  return (
    <form className="feature-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="goal">Feature Goal</label>
        <textarea
          id="goal"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Describe the feature goal in detail..."
          rows="4"
          maxLength="500"
        />
        <span className="char-count">{goal.length}/500</span>
      </div>

      <div className="form-group">
        <label>User Personas</label>
        {users.map((user, index) => (
          <div key={index} className="input-group">
            <input
              type="text"
              value={user}
              onChange={(e) => handleUserChange(index, e.target.value)}
              placeholder={`User ${index + 1}...`}
            />
            {users.length > 1 && (
              <button
                type="button"
                onClick={() => handleRemoveUser(index)}
                className="btn-remove"
              >
                ✕
              </button>
            )}
          </div>
        ))}
        {users.length < 10 && (
          <button
            type="button"
            onClick={handleAddUser}
            className="btn-secondary"
          >
            + Add User
          </button>
        )}
      </div>

      <div className="form-group">
        <label>Constraints</label>
        {constraints.map((constraint, index) => (
          <div key={index} className="input-group">
            <input
              type="text"
              value={constraint}
              onChange={(e) => handleConstraintChange(index, e.target.value)}
              placeholder={`Constraint ${index + 1}...`}
            />
            {constraints.length > 1 && (
              <button
                type="button"
                onClick={() => handleRemoveConstraint(index)}
                className="btn-remove"
              >
                ✕
              </button>
            )}
          </div>
        ))}
        {constraints.length < 10 && (
          <button
            type="button"
            onClick={handleAddConstraint}
            className="btn-secondary"
          >
            + Add Constraint
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}

      <button
        type="submit"
        className="btn-primary"
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate Feature Plan'}
      </button>
    </form>
  );
}
