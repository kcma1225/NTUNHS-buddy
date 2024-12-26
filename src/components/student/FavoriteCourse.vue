<template>
  <div class="max-w-7xl mx-auto">
    <!-- 標題區塊 -->
    <div class="h-16 bg-gradient-to-r from-green-700 to-green-900 text-white rounded-t-3xl flex items-center px-6 shadow-lg">
      <div class="mr-auto flex items-center space-x-3">
        <i class="bi bi-collection-fill text-2xl"></i>
        <span class="text-xl font-bold">收藏課程</span>
        <span class="bg-green-600 px-3 py-1 rounded-full text-sm">
          共 {{ favorites.length }} 堂課
        </span>
      </div>
    </div>

    <!-- 載入中狀態 -->
    <template v-if="loading">
      <div class="bg-white rounded-b-3xl p-10 text-center">
        <div class="text-gray-500 space-y-4">
          <div class="animate-spin inline-block w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full"></div>
          <p class="text-lg">載入中...</p>
        </div>
      </div>
    </template>

    <template v-else>
      <!-- 課程列表 -->
      <ul v-if="favorites.length" class="divide-y divide-gray-200 bg-white shadow-md rounded-b-3xl">
        <li v-for="course in favorites" 
            :key="course._id"
            class="group relative transform transition-all duration-300 hover:bg-gray-50">
          
          <div class="p-6">
            <!-- 課程標題與基本信息 -->
            <div class="flex flex-col md:flex-row justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-xl font-bold text-gray-800 group-hover:text-green-700 transition-colors mb-2">
                  {{ course.課程名稱 }}
                </h3>
                <div class="flex flex-wrap gap-2 mb-2">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800">
                    <i class="bi bi-bookmark-fill mr-2"></i>{{ course.編號 }}
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                    學期: {{ course.學期 }}
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-purple-100 text-purple-800">
                    {{ course.系所 }}
                  </span>
                </div>
              </div>

              <!-- 操作按鈕 -->
              <div class="flex gap-2 mt-2 md:mt-0">
                <button 
                  @click="removeCourse(course._id)"
                  class="inline-flex items-center justify-center px-4 py-2 rounded-full
                         bg-gradient-to-r from-red-500 to-red-600 text-white
                         hover:from-red-600 hover:to-red-700 transform hover:scale-105
                         transition duration-200 shadow-md hover:shadow-lg">
                  <i class="bi bi-trash mr-2"></i>
                  移除課程
                </button>
                <button 
                  @click="openDetails(course)"
                  class="inline-flex items-center justify-center px-4 py-2 rounded-full
                         bg-gradient-to-r from-blue-500 to-blue-600 text-white
                         hover:from-blue-600 hover:to-blue-700 transform hover:scale-105
                         transition duration-200 shadow-md hover:shadow-lg">
                  <i class="bi bi-eye mr-2"></i>
                  查看詳情
                </button>
              </div>
            </div>

            <!-- 課程詳細資訊 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- 左側資訊 -->
              <div class="space-y-2">
                <!-- 教師資訊 -->
                <div class="flex flex-wrap gap-2">
                  <template v-if="isValidTeachers(course.教師姓名)">
                    <span v-for="teacher in processedTeachers(course.教師姓名)"
                          :key="teacher"
                          class="inline-flex items-center px-3 py-1 rounded-full text-sm
                                 bg-gray-100 text-gray-700 group-hover:bg-gray-200">
                      <i class="bi bi-person-fill mr-2"></i>
                      {{ teacher }}
                    </span>
                  </template>
                  <span v-else class="inline-flex items-center px-3 py-1 rounded-full text-sm
                                   bg-gray-100 text-gray-700">
                    <i class="bi bi-person-fill mr-2"></i>查無資料
                  </span>
                </div>

                <!-- 上課時間地點 -->
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-geo-alt-fill mr-2"></i>
                  <span>{{ course.地點 }}</span>
                </div>
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-clock-fill mr-2"></i>
                  <span>星期{{ course.星期 }} | {{ course.節次 }}節</span>
                </div>
              </div>

              <!-- 右側資訊 -->
              <div class="space-y-2">
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-people-fill mr-2"></i>
                  <span>修課人數：{{ course.上課人數 }} 人</span>
                </div>
              </div>
            </div>
          </div>
        </li>
      </ul>

      <!-- 無資料顯示 -->
      <div v-else class="bg-white rounded-b-3xl p-10 text-center">
        <div class="text-gray-500 space-y-4">
          <i class="bi bi-bookmark-x text-6xl"></i>
          <p class="text-xl font-medium">無任何收藏課程</p>
          <p class="text-gray-400">快去探索更多有趣的課程吧！</p>
          <button 
            @click="goToCourseList"
            class="mt-4 inline-flex items-center justify-center px-6 py-3 rounded-full
                   bg-gradient-to-r from-green-500 to-green-600 text-white
                   hover:from-green-600 hover:to-green-700 transform hover:scale-105
                   transition duration-200 shadow-md hover:shadow-lg">
            <i class="bi bi-search mr-2"></i>
            瀏覽課程
          </button>
        </div>
      </div>
    </template>

    <!-- 課程詳情組件 -->
    <CourseDetail 
      :show="showDetail"
      :course="selectedCourse"
      @close="closeDetails"
    />
  </div>
</template>

<script>
import CourseDetail from './CourseDetail.vue'
import Cookies from "js-cookie";
import apiService from "../../api/apiService.js";

export default {
  name: "FavoriteCourse",
  components: {
    CourseDetail
  },
  data() {
    return {
      showDetail: false,
      selectedCourse: null,
      favorites: [],
      loading: true,
      error: null,
      username: null
    };
  },
  async created() {
    await this.fetchFavorites();
  },
  
  methods: {
    async fetchFavorites() {
      try {
        this.loading = true;
        this.username = Cookies.get("username");
        
        if (!this.username) {
          throw new Error("使用者未登入");
        }
        
        // 從 API 獲取響應
        const response = await apiService.getFavorite(this.username);
        
        // 使用 response 來獲取實際的回應數據
        const responseData = response;
        
        if (responseData.status === "success") {
          this.favorites = [...responseData.favorites];
          console.log('收藏課程已更新:', this.favorites);
        } else {
          throw new Error(responseData.message || "獲取收藏失敗");
        }
      } catch (error) {
        this.error = error.message;
        console.error("獲取收藏失敗:", error);
      } finally {
        this.loading = false;
      }
    },
    processedTeachers(teacherString) {
      const rawTeachers = teacherString.split("\n")[0];
      const teachers = rawTeachers
        .split(",")
        .filter((name) => name.trim() !== "")
        .map((name) => name.trim());
      return teachers.length > 4 ? teachers.slice(0, 3).concat("更多...") : teachers;
    },
    isValidTeachers(teacherString) {
      const rawTeachers = teacherString.split("\n")[0];
      return rawTeachers.split(",").some((name) => isNaN(name.trim()));
    },

    async removeCourse(courseId) {
      try {
        if (confirm('確定要移除此課程嗎？')) {
          // 調用 API 移除課程的邏輯可以在這裡添加
          await apiService.removeFavorite(this.username,courseId);
          this.favorites = this.favorites.filter(c => c._id !== courseId);
          alert('課程已移除');
        }
      } catch (error) {
        console.error("移除失敗:", error);
        alert('移除失敗，請稍後重試');
      }
    },
    openDetails(course) {
      this.selectedCourse = course;
      this.showDetail = true;
      document.body.style.overflow = 'hidden';
    },
    closeDetails() {
      this.showDetail = false;
      this.selectedCourse = null;
      document.body.style.overflow = 'auto';
    },
    goToCourseList() {
      this.$router.push('/');
    }
  }
};
</script>