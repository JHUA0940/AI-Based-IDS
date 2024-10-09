import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:4321', // Set the base URL to your Flask server
  timeout: 10000, // Request timeout setting
});

// Export API interface
export const postData = (threshold) => api.post('/update_threshold', { threshold }); // Sends data to the specified path and passes parameters