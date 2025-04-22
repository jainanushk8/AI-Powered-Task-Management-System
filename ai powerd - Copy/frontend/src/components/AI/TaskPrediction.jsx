import React, { useState } from 'react';
import { predictSchedule } from '../../api'; // Import the predictSchedule function

function TaskPrediction({ taskDescription }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getPrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      // Using the predictSchedule function from api.js to get the task prediction
      const response = await predictSchedule(taskDescription);
      setPrediction(response);
    } catch (err) {
      setError('Error fetching prediction. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="task-prediction">
      <h4>📅 Task Prediction</h4>
      <button onClick={getPrediction} disabled={loading}>
        {loading ? 'Loading...' : 'Get Prediction'}
      </button>

      {error && <p className="error">{error}</p>}

      {prediction && (
        <div>
          <p>Risk Level: {prediction.label}</p>
          <p>Confidence Scores: {prediction.confidence_scores.map((score, idx) => (
            <span key={idx}>{`C${idx}: ${(score * 100).toFixed(1)}% `}</span>
          ))}</p>
        </div>
      )}
    </div>
  );
}

export default TaskPrediction;
