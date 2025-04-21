const axios = require('axios');

const AI_SERVICE_URL = 'http://localhost:8000/api';

exports.analyzeSentiment = async (req, res) => {
  try {
    const { text } = req.body;
    const response = await axios.post(`${AI_SERVICE_URL}/sentiment`, { text });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Sentiment analysis failed', details: error.message });
  }
};

exports.optimizeTask = async (req, res) => {
  try {
    const { deadline_days, num_dependencies, current_workload } = req.body;
    const response = await axios.post(`${AI_SERVICE_URL}/optimize-task`, {
      deadline_days,
      num_dependencies,
      current_workload
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Task optimization failed', details: error.message });
  }
};

exports.scheduleAndPredict = async (req, res) => {
  try {
    const { task_description } = req.body;
    const response = await axios.post(`${AI_SERVICE_URL}/schedule-predict`, { task_description });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Schedule prediction failed', details: error.message });
  }
};
