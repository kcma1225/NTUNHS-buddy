// src/config.js
const config = {
    api: {
      ip: '54.159.83.73', // 從環境變數獲取 IP
      port: "8000", // 從環境變數獲取 Port
      baseURL: function () {
        return `http://${this.ip}:${this.port}`;
      },
    },
  };
  
  export default config;
  