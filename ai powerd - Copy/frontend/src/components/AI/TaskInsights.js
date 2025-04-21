import React, { useEffect, useState } from 'react';
import axios from 'axios';

function TaskInsights({ task }) {
  const [sentiment, setSentiment] = useState(null);
  const [priority, setPriority] = useState(null);
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    if (task) {
      axios.post('/api/ai/sentiment', { text: task.description }).then(res => setSentiment(res.data));
      axios.post('/api/ai/optimize-task', {
        deadline_days: task.deadlineDays,
        num_dependencies: task.dependencies.length,
        current_workload: task.assignedUserTaskCount
      }).then(res => setPriority(res.data));
      axios.post('/api/ai/schedule-predict', { task_description: task.description }).then(res => setSchedule(res.data));
    }
  }, [task]);

  return (
    <div className="task-insights">
      <h4>🧠 AI Insights</h4>
      {sentiment && <p>Sentiment: {sentiment.label} ({(sentiment.confidence * 100).toFixed(1)}%)</p>}
      {priority && <p>Priority Score: {priority.priority_score.toFixed(2)}</p>}
      {schedule && (
        <p>Schedule Suggestion: Risk Level {schedule.label} <br />
        Confidence: {schedule.confidence_scores.map((c, i) => `C${i}: ${(c * 100).toFixed(1)}% `).join(' ')}</p>
      )}
    </div>
  );
}

export default TaskInsights;
