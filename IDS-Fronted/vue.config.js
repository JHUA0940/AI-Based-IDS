const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/socket.io': {
        target: 'http://localhost:4321', // Replace with your Flask-SocketIO server address
        ws: true, // Enable the WebSocket proxy
        changeOrigin: true
      },
      // '/': {
      //   target: 'http://localhost:4321', // Flask server address
      //   changeOrigin: true, // Make sure the source in the request header is set correctly
      //   pathRewrite: { '^/': '' }, // Rewrite URL path to match Flask's endpoint
      // },
      '/update_threshold': { // Explicitly define this endpoint
        target: 'http://localhost:4321', // Target Flask server
        changeOrigin: true, // Change the origin of the host header
        pathRewrite: { '^/update_threshold': '/update_threshold' }, // Rewrite the path if needed
      },
    },
  }
})
