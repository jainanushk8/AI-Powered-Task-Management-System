import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const DashboardCharts = ({ stats }) => {
  const barData = {
    labels: ['Completed', 'Pending', 'Overdue'],
    datasets: [{
      label: 'Tasks',
      data: [stats.completed, stats.pending, stats.overdue],
      backgroundColor: ['#4caf50', '#ff9800', '#f44336']
    }]
  };

  const pieData = {
    labels: ['Low', 'Medium', 'High'],
    datasets: [{
      data: [stats.low, stats.medium, stats.high],
      backgroundColor: ['#2196f3', '#ffc107', '#f44336']
    }]
  };

  return (
    <div className="dashboard-charts">
      <Bar data={barData} />
      <Pie data={pieData} />
    </div>
  );
};

export default DashboardCharts;
