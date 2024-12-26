<template>
    <div>
      <!-- 上傳學生資料檔案的按鈕 -->
      <input 
        type="file" 
        accept="application/json" 
        class="hidden" 
        ref="fileInput" 
        @change="handleFileUpload"
      />
      <button 
        class="bg-blue-500 text-white px-4 py-2 rounded mb-4 hover:bg-blue-600" 
        @click="triggerFileInput">
        上傳學生資料檔案
      </button>
  
      <!-- 提示框 -->
      <div 
        v-if="alert.message" 
        :class="alert.class" 
        class="p-4 rounded fixed top-4 right-4 z-50 shadow-lg">
        {{ alert.message }}
      </div>
  
      <!-- 搜尋欄位 -->
      <div class="flex items-center rounded border border-gray-300 p-2 w-full max-w-md mb-4 mx-auto">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="搜尋..."
          class="flex-grow outline-none px-2"
        />
        <i 
          class="bi bi-search text-gray-500 cursor-pointer"
          @click="performSearch"
        ></i>
      </div>
  
      <!-- 學生姓名顯示 -->
      <div v-if="studentName" class="text-center mt-4">
        <p class="text-xl font-bold">學生姓名：{{ studentName }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import apiService from "../../api/apiService.js";
  
  export default {
    name: "StudentManagement",
    data() {
      return {
        searchQuery: "", // 綁定搜尋欄位的內容
        alert: { message: "", class: "" }, // 提示框內容
        studentName: "", // 學生姓名
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
  
        if (file.type !== "application/json") {
          this.showAlert("上傳檔案非JSON檔", "bg-red-500 text-white");
          return;
        }
  
        const formData = new FormData();
        formData.append("file", file); // 直接將 JSON 文件以 blob 格式附加
  
        this.uploadJsonData(formData);
      },
      uploadJsonData(formData) {
        apiService.uploadStudentData(formData)
          .then(() => {
            this.showAlert("上傳成功", "bg-green-500 text-white");
          })
          .catch((error) => {
            const errorMessage = error.response?.data?.detail || "上傳失敗";
            this.showAlert(errorMessage, "bg-red-500 text-white");
          });
      },
      performSearch() {
        if (!this.searchQuery) {
          this.showAlert("請輸入帳號進行搜尋", "bg-red-500 text-white");
          return;
        }
  
        apiService.getStudentDetails({ account: this.searchQuery })
          .then((response) => {
            this.studentName = response.data.student_details.name;
            this.showAlert("搜尋成功", "bg-green-500 text-white");
          })
          .catch((error) => {
            const errorMessage = error.response?.data?.detail || "搜尋失敗";
            this.showAlert(errorMessage, "bg-red-500 text-white");
          });
      },
      showAlert(message, alertClass) {
        this.alert.message = message;
        this.alert.class = alertClass;
        setTimeout(() => {
          this.alert.message = "";
          this.alert.class = "";
        }, 3000);
      },
    },
  };
  </script>
  
  <style scoped>
  button {
    transition: background-color 0.3s ease;
  }
  input {
    border: none;
  }
  .bg-green-500 {
    background-color: #48bb78; /* Tailwind green-500 */
  }
  .bg-red-500 {
    background-color: #f56565; /* Tailwind red-500 */
  }
  </style>
  