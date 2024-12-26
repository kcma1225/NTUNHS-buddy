<template>
  <div class="mx-auto max-w-4xl p-4">
    <!-- 標題 -->
    <h1 class="text-2xl font-bold mb-4 text-center">課程管理</h1>

    <!-- 只保留上傳課程資料的按鈕，置中顯示 -->
    <div class="flex flex-col items-center justify-center">
      <!-- 隱藏的檔案上傳 input -->
      <input
        type="file"
        accept="application/json"
        class="hidden"
        ref="fileInput"
        @change="handleFileUpload"
      />
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        @click="triggerFileInput"
      >
        上傳課程資料
      </button>
    </div>

    <!-- 提示訊息（alert），使用過渡效果 -->
    <transition name="fade">
      <div
        v-if="alert.message"
        :class="alert.class"
        class="p-4 rounded fixed top-4 right-4 z-50 shadow-lg"
      >
        {{ alert.message }}
      </div>
    </transition>

    <!-- 課程顯示區域 -->
    <div v-if="courseName" class="mt-4 border rounded p-4 bg-white shadow">
      <p class="text-xl font-bold mb-2">課程名稱：{{ courseName }}</p>
      <p class="text-gray-700 mb-1">課程描述：{{ courseDescription }}</p>
      <p class="text-gray-700">講師：{{ instructor }}</p>
    </div>

    <!-- 尚未顯示課程時的提示 -->
    <div v-else class="text-center text-gray-500 mt-4">
      <p>可上傳 JSON 檔案，新增課程。</p>
    </div>
  </div>
</template>

<script>
import apiService from '../../api/apiService';

export default {
  name: "CourseManagement",
  data() {
    return {
      // 提示訊息物件
      alert: { message: "", class: "" },
      // 課程顯示資料
      courseName: "",
      courseDescription: "",
      instructor: "",
    };
  },
  methods: {
    // 觸發檔案上傳
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    // 監聽檔案上傳事件
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // 僅接受 JSON
      if (file.type !== "application/json") {
        this.showAlert("上傳檔案非JSON格式", "bg-red-500 text-white");
        return;
      }

      // 將檔案包裝成 FormData
      const formData = new FormData();
      formData.append("file", file);

      this.uploadJsonData(formData);
    },
    // 呼叫 API 上傳課程資料
    uploadJsonData(formData) {
      apiService
        .uploadCourseData(formData)
        .then(() => {
          this.showAlert("課程資料上傳成功", "bg-green-500 text-white");
          // 在此可根據回傳資料設置課程名稱等資訊
          // e.g. this.courseName = ...
        })
        .catch((error) => {
          const errorMessage = error.response?.data?.detail || "上傳失敗";
          this.showAlert(errorMessage, "bg-red-500 text-white");
        });
    },
    // 顯示提示訊息
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
/* 按鈕 hover 效果 */
button {
  transition: background-color 0.3s ease;
}

/* 隱藏 input 預設邊框 */
input {
  border: none;
}

/* 過渡效果 (alert 出現 / 消失) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* 自訂提示訊息顏色 */
.bg-green-500 {
  background-color: #48bb78; /* Tailwind green-500 */
}
.bg-red-500 {
  background-color: #f56565; /* Tailwind red-500 */
}
</style>
