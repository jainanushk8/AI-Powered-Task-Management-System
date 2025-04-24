import axios from 'axios';

const testOptimizeTask = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/optimize-task/', {
      deadline_days: 5,
      num_dependencies: 3,
      current_workload: 7
    });
    console.log('Optimize Task Response:', response.data);
  } catch (error) {
    console.error('Error in optimizeTask:', error.response?.data || error.message);
  }
};

testOptimizeTask();
