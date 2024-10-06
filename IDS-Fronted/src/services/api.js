import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:4321', // Set the base URL to your Flask server
  timeout: 10000, // 请求超时设置
});

// 导出 API 接口
export const postData = (threshold) => api.post('/update_threshold', { threshold }); // 发送数据到指定路径，并传递参数