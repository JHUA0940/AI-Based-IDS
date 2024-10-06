import axios from 'axios';

// 创建 Axios 实例
const api = axios.create({
  baseURL: '/', // 后端接口的基地址
  timeout: 10000, // 请求超时设置
});

// 导出 API 接口
export const postData = (threshold) => api.post('/update_threshold', { threshold }); // 发送数据到指定路径，并传递参数