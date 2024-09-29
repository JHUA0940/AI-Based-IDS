const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'http://localhost:4321', // 替换为你的 Flask-SocketIO 服务器地址
        ws: true, // 启用 WebSocket 代理
        changeOrigin: true
      }
    }
  }
})
