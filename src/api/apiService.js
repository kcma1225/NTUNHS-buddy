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
 // 上傳課程資料 API 請求
 uploadCourseData(formData) {
  return apiClient.post("/import-courses", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      "accept": "application/json",
    },
  });
},
 // 上傳課程資料 API 請求
 deleteCourse(courseId){
  return apiClient.post(`/delete-course?course_id=${courseId}`,{   
    headers: {
    "accept": "application/json",
    },
  })
},
  // 獲取學生詳情 API 請求
  getStudentDetails(data) {
    return apiClient.post("/get-student-details", data, {
      headers: {
        "accept": "application/json",
      },
    });
  },

  updateFavorite(studentId,courseId){
    return apiClient.post(`/add-to-favorites?account_id=${studentId}&course_id=${courseId}`,{   
      headers: {
      "accept": "application/json",
      },
    })
  },

  getFavorite(account_id) {
    return apiClient.get(`get-favorites-details?account_id=${account_id}`, {   
      headers: {
        "accept": "application/json",
      },
    }).then(response => response.data);  // 直接返回數據部分
  },

  removeFavorite(account_id,course_id){
    return apiClient.post(`/remove-from-favorites?account_id=${account_id}&course_id=${course_id}`,{
      headers: {
        "accept": "application/json",
      },
    })
  },
    // 改密碼
  ChangePassword(data) {
    return apiClient.post("/change-password", data, {
      headers: {
        "accept": "application/json",
      },
    });
  },
};
