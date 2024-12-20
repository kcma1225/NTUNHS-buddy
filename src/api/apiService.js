// src/api/apiService.js
import axios from "axios";
import config from "@/api/config.js"; // 引入 config.js

const apiClient = axios.create({
  baseURL: config.api.baseURL(), // 使用 baseURL
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  // 範例 API 請求：獲取資料
  getExampleData() {
    return apiClient.get("/example-endpoint");
  },

  // 範例 API 請求：發送資料
  postExampleData(data) {
    return apiClient.post("/example-endpoint", data);
  },
};
