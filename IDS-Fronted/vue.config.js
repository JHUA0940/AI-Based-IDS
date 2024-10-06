const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'http://localhost:4321', // 替换为你的 Flask-SocketIO 服务器地址
        ws: true, // 启用 WebSocket 代理
        changeOrigin: true
      },
      '/': {
        target: 'http://localhost:4321', // 代理到 Flask 服务器地址
        changeOrigin: true, // 确保请求头中的来源被正确设置
        ws: false, // 启用 WebSocket 支持
      }
    },
  }
})
