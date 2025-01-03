<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header Section -->
    <div class="bg-green-800 text-white rounded-t-3xl flex items-center px-6 py-4 shadow-lg">
      <div class="text-lg font-semibold flex items-center space-x-2">
        <span>課程列表</span>
        <span class="bg-green-700 px-3 py-1 rounded-full text-sm">
          共{{ 課程列表.length }}堂課
        </span>
      </div>
    </div>

    <!-- Course List Section -->
    <ul v-if="課程列表.length" class="course-list bg-white shadow-md rounded-b-3xl divide-y divide-gray-200">
      <li
        v-for="course in 課程列表"
        :key="course._id"
        @click="openDetails(course)"
        class="flex flex-col lg:flex-row items-start lg:items-center p-6 hover:bg-gray-50 transition-colors duration-200 gap-6"
      >
        <!-- Left Section -->
        <div class="text-sm text-gray-600 lg:w-1/6 flex flex-col space-y-1">
          <div class="bg-green-50 px-3 py-1 rounded-lg inline-flex">{{ course.年級 }}年級</div>
          <div>學期: {{ course.學期 }}</div>
          <div>科目代號: {{ course.科目代號 }}</div>
        </div>

        <!-- Center Section -->
        <div class="flex-1 space-y-3">
          <div class="text-xl font-bold text-green-800">{{ course.課程名稱 }}</div>
          <div class="flex flex-wrap gap-2">
            <template v-if="isValidTeachers(course.教師姓名)">
              <span
                v-for="(teacher, index) in processedTeachers(course.教師姓名)"
                :key="teacher"
                class="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700 shadow-sm"
              >
                <i class="bi bi-person-fill mr-2"></i>
                <span v-if="index < 3">{{ teacher }}</span>
                <span v-else-if="index === 3">更多...</span>
              </span>
            </template>
            <span v-else class="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700 shadow-sm">
              <i class="bi bi-person-fill mr-2"></i>查無資料
            </span>
          </div>
        </div>

        <!-- Middle Section -->
        <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-700">
          <span class="flex items-center bg-blue-50 rounded-lg px-3 py-2">
            <i class="bi bi-people-fill mr-2 text-blue-600"></i>{{ course.上課人數 }}人
          </span>
          <span class="flex items-center bg-purple-50 rounded-lg px-3 py-2">
            <i class="bi bi-geo-alt-fill mr-2 text-purple-600"></i>地點: {{ course.地點 }}
          </span>
          <span class="flex items-center bg-orange-50 rounded-lg px-3 py-2">
            <i class="bi bi-clock mr-2 text-orange-600"></i>時間: 星期{{ course.星期 }} | {{ formatPeriod(course.節次) }}節
          </span>
        </div>

        <!-- Right Section -->
        <div class="flex flex-col sm:flex-row lg:w-1/6 gap-3 w-full lg:justify-end">
          <!-- 若 role !== 'admin'，顯示「加入排課」與「加入收藏」 -->
          <template v-if="cookiesData.role !== 'admin'">
            <button
              @click.stop="addToSchedule(course)"
              class="w-full sm:w-auto px-6 py-2 text-sm text-white bg-green-600 rounded-full hover:bg-green-700 transition-colors duration-200 shadow-md hover:shadow-lg"
            >
              加入排課
            </button>
            <button
              @click.stop="addToFavorites(course)"
              class="w-full sm:w-auto px-6 py-2 text-sm text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-colors duration-200 shadow-md hover:shadow-lg"
            >
              加入收藏
            </button>
          </template>

          <!-- 若 role === 'admin'，顯示「刪除課程」 -->
          <button
            v-else
            @click.stop="deleteCourse(course)"
            class="w-full sm:w-auto px-6 py-2 text-sm text-white bg-red-600 rounded-full hover:bg-red-700 transition-colors duration-200 shadow-md hover:shadow-lg"
          >
            刪除課程
          </button>
        </div>
      </li>
    </ul>
    <div v-else class="bg-white rounded-b-3xl text-center text-gray-500 py-10 shadow-md">
      目前沒有任何課程資料。
    </div>

    <!-- Back to Top Button -->
    <button
      v-show="showBackToTop"
      @click="scrollToTop"
      class="fixed bottom-8 right-8 px-4 py-2 bg-green-600 text-white rounded-full shadow-lg hover:bg-green-700 transition-colors duration-200 z-50"
    >
      <i class="bi bi-arrow-up mr-2"></i>回到頂端
    </button>

    <!-- Popup Details Component -->
    <CourseDetails v-if="showDetails" :course="selectedCourse" @close="closeDetails" />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../api/config.js";
import CourseDetails from "./CourseDetails.vue";
import apiService from "../../api/apiService.js";

const apiClient = axios.create({
  baseURL: config.api.baseURL(),
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  props: {
    filters: { type: Object, required: true },
  },
  components: {
    CourseDetails,
  },
  data() {
    return {
      課程列表: [],
      showBackToTop: false,
      showDetails: false,
      selectedCourse: null,
      cookiesData: this.getCookiesData(),
    };
  },
  watch: {
    filters: {
      immediate: true,
      deep: true,
      handler(newFilters) {
        this.fetchCourses(newFilters);
      },
    },
  },
  methods: {
    async fetchCourses(filters) {
      try {
        const filteredParams = Object.entries(filters)
          .filter(([key, value]) => value !== null && value !== "")
          .reduce((acc, [key, value]) => {
            acc[key] = value;
            return acc;
          }, {});
        const urlParams = new URLSearchParams(filteredParams).toString();
        const response = await apiClient.get(`/final-course-selection?${urlParams}`);
        this.課程列表 = response.data.results;
      } catch (error) {
        console.error("Failed to fetch courses:", error);
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
    formatPeriod(periodString) {
      const periods = periodString.split(",").map((p) => parseInt(p, 10));
      return `${Math.min(...periods)}-${Math.max(...periods)}`;
    },
    openDetails(course) {
      this.selectedCourse = course;
      this.showDetails = true;
    },
    closeDetails() {
      this.selectedCourse = null;
      this.showDetails = false;
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    handleScroll() {
      this.showBackToTop = window.scrollY > 200;
    },
    addToSchedule(course) {
      if (!Cookies.get('role')){
        alert('請先登入');
        return
      }
      const currentCourses = JSON.parse(localStorage.getItem('selectedCourses') || '[]');
      
      const hasConflict = this.checkTimeConflict(course, currentCourses);
      if (hasConflict) {
        alert('課程時間衝突！無法加入此課程。');
        return;
      }

      if (currentCourses.some(c => c._id === course._id)) {
        alert('此課程已經加入！');
        return;
      }

      currentCourses.push(course);
      localStorage.setItem('selectedCourses', JSON.stringify(currentCourses));
      
      this.$emit('course-added');
      alert('成功加入課程！');
    },
    checkTimeConflict(newCourse, existingCourses) {
      const newCourseSlots = newCourse.節次.split(',').map(slot => ({
        day: newCourse.星期,
        slot: parseInt(slot)
      }));

      return existingCourses.some(existingCourse => {
        const existingSlots = existingCourse.節次.split(',').map(slot => ({
          day: existingCourse.星期,
          slot: parseInt(slot)
        }));

        return newCourseSlots.some(newSlot => 
          existingSlots.some(existingSlot => 
            newSlot.day === existingSlot.day && 
            newSlot.slot === existingSlot.slot
          )
        );
      });
    },
    addToFavorites(course) {
      if (!Cookies.get('role')){
        alert('請先登入');
        return
      }
      apiService.updateFavorite(this.cookiesData.username, course._id)
        .then(() => {
          alert(`成功加入課程: ${course.課程名稱}`);
        })
        .catch((error) => {
          const errorMessage = error.response?.data?.detail || "加入失敗";
          alert(errorMessage);
        });
    },
    deleteCourse(course) {
      const isConfirmed = confirm(
        `確定要刪除「${course.課程名稱}」嗎？\n此動作無法恢復，請謹慎操作。`
      );
      if (!isConfirmed) return;

      apiService.deleteCourse(course._id)
        .then(() => {
          alert(`成功刪除課程: ${course.課程名稱}`);
          location.reload();
        })
        .catch((error) => {
          const errorMessage = error.response?.data?.detail || "刪除失敗";
          alert(errorMessage);
        });
    },
    getCookiesData() {
      return {
        name: Cookies.get("name"),
        username: Cookies.get("username"),
        role: Cookies.get("role"),
        token: Cookies.get("auth_token"),
      };
    },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
.course-list {
  list-style-type: none;
}
</style>