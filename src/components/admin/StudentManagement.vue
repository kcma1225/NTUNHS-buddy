<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- 檔案上傳區域 -->
    <div class="mb-8">
      <input 
        type="file" 
        accept="application/json" 
        class="hidden" 
        ref="fileInput" 
        @change="handleFileUpload"
      />
      <button 
        class="flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg hover:bg-blue-700 shadow-sm transition-colors"
        @click="triggerFileInput"
      >
        <i class="bi bi-cloud-upload text-lg"></i>
        <span class="font-medium">上傳學生資料檔案</span>
      </button>
    </div>

    <!-- 提示框 -->
    <div 
      v-if="alert.message" 
      :class="[
        alert.class,
        'fixed top-6 right-6 z-50 px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 transition-all duration-300'
      ]"
    >
      <i :class="[
        'bi',
        alert.class.includes('green') ? 'bi-check-circle' : 'bi-exclamation-circle'
      ]"></i>
      {{ alert.message }}
    </div>

    <!-- 搜尋區塊 -->
    <div class="mb-8">
      <div class="flex items-center bg-white rounded-lg border border-gray-200 hover:border-blue-400 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all duration-200">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="輸入學生帳號進行搜尋..."
          class="flex-grow px-4 py-3 text-gray-700 placeholder-gray-400 bg-transparent rounded-lg focus:outline-none"
        />
        <button 
          class="px-4 py-3 text-gray-500 hover:text-blue-600 transition-colors"
          @click="performSearch"
        >
          <i class="bi bi-search text-lg"></i>
        </button>
      </div>
    </div>

    <!-- 學生資訊卡片 -->
    <div 
      v-if="studentName" 
      class="bg-white rounded-lg border border-gray-200 p-6 shadow-sm"
    >
      <div class="flex flex-col md:flex-row gap-6">
        <!-- 學生照片 -->
        <div class="w-full md:w-1/3">
          <div class="relative pt-[100%] rounded-lg overflow-hidden bg-gray-100">
            <img
              :src="studentImageUrl"
              :alt="studentName"
              class="absolute inset-0 w-full h-full object-cover"
              @error="handleImageError"
            />
          </div>
        </div>
        
        <!-- 學生資訊 -->
        <div class="w-full md:w-2/3 space-y-4">
          <div>
            <h3 class="text-sm text-gray-500 font-medium">學生姓名</h3>
            <p class="text-lg text-gray-800 font-semibold">{{ studentName }}</p>
          </div>
          <div>
            <h3 class="text-sm text-gray-500 font-medium">學號</h3>
            <p class="text-lg text-gray-800 font-semibold">{{ searchQuery }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from "../../api/apiService.js";

export default {
  name: "StudentManagement",
  data() {
    return {
      searchQuery: "",
      alert: { message: "", class: "" },
      studentName: "",
      imageError: false,
      studentImageUrl: "" // 新增: 儲存學生圖片 URL
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
      formData.append("file", file);

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
          this.imageError = false;
          // 搜尋成功時更新圖片 URL
          this.studentImageUrl = `https://system8.ntunhs.edu.tw/IntranetImage/111/${this.searchQuery}.jpg`;
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
    handleImageError(e) {
      // 當圖片載入失敗時，替換為預設圖片
      e.target.src = 'path/to/default-avatar.png';  // 請替換成您的預設圖片路徑
      this.imageError = true;
    }
  },
};
</script>

<style scoped>
button {
  transition: all 0.2s ease;
}
button:active {
  transform: translateY(1px);
}
.bg-green-500 {
  background-color: #48bb78;
}
.bg-red-500 {
  background-color: #f56565;
}
</style>