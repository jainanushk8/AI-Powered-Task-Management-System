// src/App.js
import React from 'react';
import TaskPrediction from './components/TaskPrediction';  // Import the TaskPrediction component
import TaskInsights from './components/TaskInsights';      // Assuming you already have this

function App() {
  // Sample task object (you can replace this with real task data)
  const task = {
    description: "Task is taking longer than expected due to multiple delays in frontend implementation.",
    deadlineDays: 5,
    dependencies: ["Dependency 1", "Dependency 2"],  // Just example dependencies
    assignedUserTaskCount: 3
  };

  return (
    <div className="App">
      <h1>Task Insights</h1>
      
      {/* Pass the task object as a prop to TaskInsights */}
      <TaskInsights task={task} />

      {/* Pass task description as a prop to TaskPrediction */}
      <TaskPrediction taskDescription={task.description} />
    </div>
  );
}

export default App;
