// src/api.js
import axios from 'axios';

// Create an axios instance with your base URL
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/ai', // Change this to your backend API URL
});

// Function to get sentiment analysis
export const getSentiment = async (text) => {
  try {
    const response = await api.post('/sentiment', { text });
    return response.data;
  } catch (error) {
    throw new Error('Error fetching sentiment analysis');
  }
};

// Function to optimize task based on provided data
export const optimizeTask = async (taskData) => {
  try {
    const response = await api.post('/optimize-task', taskData);
    return response.data;
  } catch (error) {
    throw new Error('Error optimizing task');
  }
};

// Function to predict the schedule based on task description
export const predictSchedule = async (taskDescription) => {
  try {
    const response = await api.post('/schedule-predict', { task_description: taskDescription });
    return response.data;
  } catch (error) {
    throw new Error('Error predicting schedule');
  }
};
