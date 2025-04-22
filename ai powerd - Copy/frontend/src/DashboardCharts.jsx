// src/components/DashboardCharts.jsx
import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from 'chart.js';

// Register the necessary ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const DashboardCharts = ({ stats }) => {
  // Ensure the stats prop is properly passed, if not set defaults
  const barData = {
    labels: ['Completed', 'Pending', 'Overdue'],
    datasets: [{
      label: 'Tasks',
      data: [stats?.completed || 0, stats?.pending || 0, stats?.overdue || 0], // Handle potential undefined stats
      backgroundColor: ['#4caf50', '#ff9800', '#f44336']
    }]
  };

  const pieData = {
    labels: ['Low', 'Medium', 'High'],
    datasets: [{
      data: [stats?.low || 0, stats?.medium || 0, stats?.high || 0], // Handle potential undefined stats
      backgroundColor: ['#2196f3', '#ffc107', '#f44336']
    }]
  };

  return (
    <div className="dashboard-charts">
      <div className="chart-container">
        <Bar data={barData} />
      </div>
      <div className="chart-container">
        <Pie data={pieData} />
      </div>
    </div>
  );
};

export default DashboardCharts;
