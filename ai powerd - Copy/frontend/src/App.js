import React, { useState, useEffect } from 'react';
import axios from 'axios';  // Import axios for API requests
import TaskPrediction from './components/TaskPrediction';  // Import TaskPrediction
import TaskInsights from './components/TaskInsights';      // Import TaskInsights
import ChatBox from "./components/ChatBox";                  // Import ChatBox

function App() {
  const [task, setTask] = useState(null);  // State to store the task data
  const [loading, setLoading] = useState(true);  // Loading state

  // Fetch real task data from the backend
  useEffect(() => {
    const fetchTaskData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/tasks/1');  // Replace with your task API endpoint
        setTask(response.data);  // Update state with the task data
      } catch (error) {
        console.error("Error fetching task data", error);
      } finally {
        setLoading(false);  // Set loading to false after the data is fetched
      }
    };

    fetchTaskData();  // Fetch the task data when the component mounts
  }, []);

  if (loading) {
    return <div>Loading...</div>;  // Show loading message while waiting for data
  }

  return (
    <div className="App">
      {/* Task Insights & Prediction */}
      <h1>Task Insights</h1>
      <TaskInsights task={task} />  {/* Pass task object as prop */}
      <TaskPrediction taskDescription={task.description} />  {/* Pass task description */}

      {/* ChatBox at the bottom-right of the app */}
      <div style={{ position: "fixed", bottom: 10, right: 10 }}>
        <ChatBox />
      </div>
    </div>
  );
}

export default App;
