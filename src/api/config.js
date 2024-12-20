// src/config.js
const config = {
    api: {
      ip: '192.168.1.107', // 從環境變數獲取 IP
      port: "8000", // 從環境變數獲取 Port
      baseURL: function () {
        return `http://${this.ip}:${this.port}`;
      },
    },
  };
  
  export default config;
  