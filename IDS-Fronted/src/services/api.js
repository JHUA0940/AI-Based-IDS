import axios from 'axios';

// 创建 Axios 实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:4321', // 后端接口的基地址
  timeout: 10000, // 请求超时设置
});

// 导出 API 接口
export const getData = () => api.get(''); // 示例：获取数据
export const postData = (data) => api.post('', data); // 示例：发送数据