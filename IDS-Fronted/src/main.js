import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import { io } from 'socket.io-client';
// createApp(App).mount('#app')
const app = createApp(App);
// Connect to the Socket.IO server through the proxy
const socket = io('/socket.io'); // Use relative path to go through the proxy
app.config.globalProperties.$socket = socket; // Make socket available globally
app.use(ElementPlus);
app.mount('#app');
