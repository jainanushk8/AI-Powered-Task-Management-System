import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import EmployeeList from "./components/EmployeeList";
import AssignTask from "./components/AssignTask";
import Tabs from "./components/tabs";
import "./App.css";               // ← fixed path
import ChatBox from "./components/ChatBox";
import DashboardCharts from "./DashboardCharts";
import TaskInsights from "./components/AI/TaskInsights";
import TaskPrediction from "./components/AI/TaskPrediction";
import axios from "axios";

function App() {
  // Example: Fetch a single task
  const [task, setTask] = useState(null);
  const [loadingTask, setLoadingTask] = useState(true);
  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loadingEmp, setLoadingEmp] = useState(true);
  const [errorEmp, setErrorEmp] = useState("");

  // Fetch real task data
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/tasks/1")
      .then(res => setTask(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoadingTask(false));
  }, []);

  // Fetch employee list
  useEffect(() => {
    fetch("http://localhost:5500/api/emp/empList")
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch employees");
        return res.json();
      })
      .then(data => setEmployees(data))
      .catch(err => setErrorEmp(err.message))
      .finally(() => setLoadingEmp(false));
  }, []);

  const changeTaskStatus = (id, newStatus) =>
    setTasks(tasks.map(t => t.id === id ? { ...t, status: newStatus } : t));

  if (loadingTask || loadingEmp) return <p>Loading...</p>;
  if (errorEmp) return <p style={{ color: "red" }}>Error: {errorEmp}</p>;

  return (
    <div id="container" className="bg-gray-100 h-screen">
      <Header />

      <div className="w-10/12 m-auto">
        <main id="main" className="flex justify-between mb-10">
          <EmployeeList />
          <AssignTask employees={employees} />
        </main>

        <Tabs
          employees={employees}
          tasks={tasks}
          changeTaskStatus={changeTaskStatus}
        />

        {/* AI-Powered Task Insights & Prediction */}
        <section className="my-8">
          <h1 className="text-2xl font-bold mb-4">Task Insights</h1>
          {task && (
            <>
              <TaskInsights task={task} />
              <TaskPrediction taskDescription={task.description} />
            </>
          )}
        </section>

        {/* Dashboard Analytics */}
        <section className="my-8">
          <h1 className="text-2xl font-bold mb-4">Dashboard Analytics</h1>
          <DashboardCharts
            stats={{
              completed: tasks.filter(t => t.status === "completed").length,
              pending: tasks.filter(t => t.status === "pending").length,
              overdue: tasks.filter(t => t.status === "overdue").length,
              low: 5,    // Replace with real stats
              medium: 10,
              high: 8
            }}
          />
        </section>
      </div>

      {/* Floating Chat */}
      <div style={{ position: "fixed", bottom: 10, right: 10 }}>
        <ChatBox />
      </div>
    </div>
  );
}

export default App;
