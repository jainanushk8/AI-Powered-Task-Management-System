import React, { useEffect, useState } from 'react';
import { getSentiment, optimizeTask, predictSchedule } from '../api'; // Import the API functions

function TaskInsights({ task }) {
  const [sentiment, setSentiment] = useState(null);
  const [priority, setPriority] = useState(null);
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  useEffect(() => {
    if (task) {
      setLoading(true);
      setError(null); // Clear previous errors

      // Fetch sentiment analysis
      getSentiment(task.description)
        .then(res => setSentiment(res))
        .catch(err => setError('Error fetching sentiment analysis'))
        .finally(() => setLoading(false));

      // Fetch task optimization
      optimizeTask({
        deadline_days: task.deadlineDays,
        num_dependencies: task.dependencies.length,
        current_workload: task.assignedUserTaskCount
      })
        .then(res => setPriority(res))
        .catch(err => setError('Error optimizing task'))
        .finally(() => setLoading(false));

      // Fetch schedule prediction
      predictSchedule(task.description)
        .then(res => setSchedule(res))
        .catch(err => setError('Error predicting schedule'))
        .finally(() => setLoading(false));
    }
  }, [task]);

  if (loading) {
    return <p>Loading AI insights...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="task-insights">
      <h4>🧠 AI Insights</h4>
      
      {sentiment && (
        <p>Sentiment: {sentiment.label} ({(sentiment.confidence * 100).toFixed(1)}%)</p>
      )}

      {priority && (
        <p>Priority Score: {priority.priority_score.toFixed(2)}</p>
      )}

      {schedule && (
        <p>Schedule Suggestion: Risk Level {schedule.label} <br />
          Confidence: {schedule.confidence_scores.map((c, i) => `C${i}: ${(c * 100).toFixed(1)}% `).join(' ')}
        </p>
      )}
    </div>
  );
}

export default TaskInsights;
