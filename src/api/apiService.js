// src/api/apiService.js
import axios from "axios";
import config from "./config.js"; // 引入 config.js

const apiClient = axios.create({
  baseURL: config.api.baseURL(), // 使用 baseURL
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, 
});

export default {
  // 登入 API 請求
  login(data) {
    return apiClient.post("/login", data); // 傳送登入資料至 /login
  },
  
  // 上傳學生資料 API 請求
uploadStudentData(formData) {
  return apiClient.post("/upload-students", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      "accept": "application/json",
    },
  });
},
  // 獲取學生詳情 API 請求
  getStudentDetails(data) {
    return apiClient.post("/get-student-details", data, {
      headers: {
        "accept": "application/json",
      },
    });
  },

  
};
