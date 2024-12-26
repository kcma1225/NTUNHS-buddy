<template>
    <div v-if="show" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
         @click="$emit('close')">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4"
           @click.stop>
        <!-- 標題區塊 -->
        <div class="bg-gradient-to-r from-green-700 to-green-900 text-white px-6 py-4 rounded-t-2xl flex items-center justify-between">
          <h3 class="text-xl font-bold">課程詳情</h3>
          <button @click="$emit('close')" 
                  class="text-white hover:text-green-200 transition-colors">
            <i class="bi bi-x-lg text-xl"></i>
          </button>
        </div>
  
        <!-- 詳情內容 -->
        <div class="p-6 space-y-6">
          <div class="space-y-4">
            <h4 class="text-2xl font-bold text-gray-800">{{ course.課程名稱 }}</h4>
            
            <!-- 基本資訊 -->
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-bookmark mr-2"></i>
                  編號：{{ course.編號 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-calendar3 mr-2"></i>
                  學期：{{ course.學期 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-building mr-2"></i>
                  系所：{{ course.系所 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-mortarboard mr-2"></i>
                  年級：{{ course.年級 }}年級
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-people mr-2"></i>
                  班組：{{ course.班組 }}
                </p>
              </div>
              <div class="space-y-2">
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-hash mr-2"></i>
                  科目代號：{{ course.科目代號 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-book mr-2"></i>
                  學分數：{{ course.學分數 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-journal-text mr-2"></i>
                  課別：{{ course.課別 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-person-badge mr-2"></i>
                  上課人數：{{ course.上課人數 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-tags mr-2"></i>
                  課程內容分類：{{ course.課程內容分類 }}
                </p>
              </div>
            </div>
  
            <!-- 上課資訊 -->
            <div class="border-t pt-4">
              <h5 class="font-semibold text-gray-700 mb-3">上課資訊</h5>
              <div class="grid grid-cols-2 gap-4">
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-geo-alt mr-2"></i>
                  地點：{{ course.地點 }}
                </div>
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-clock mr-2"></i>
                  時間：星期{{ course.星期 }} | {{ course.節次 }}節
                </div>
              </div>
            </div>
  
            <!-- 教師資訊 -->
            <div class="border-t pt-4">
              <h5 class="font-semibold text-gray-700 mb-3">授課教師</h5>
              <div class="flex flex-wrap gap-2">
                <template v-if="isValidTeachers(course.教師姓名)">
                  <span v-for="teacher in processedTeachers(course.教師姓名)"
                        :key="teacher"
                        class="inline-flex items-center px-3 py-1 rounded-full
                               bg-green-50 text-green-700">
                    <i class="bi bi-person-fill mr-2"></i>
                    {{ teacher }}
                  </span>
                </template>
                <span v-else class="inline-flex items-center px-3 py-1 rounded-full
                                 bg-gray-100 text-gray-700">
                  <i class="bi bi-person-fill mr-2"></i>查無資料
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CourseDetail',
    props: {
      show: {
        type: Boolean,
        required: true
      },
      course: {
        type: Object,
        required: true,
        default: () => ({})
      }
    },
    mounted() {
      window.addEventListener('keydown', this.handleEscKey);
    },
    beforeDestroy() {
      window.removeEventListener('keydown', this.handleEscKey);
    },
    methods: {
      handleEscKey(e) {
        if (e.key === 'Escape' && this.show) {
          this.$emit('close');
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
    }
  };
  </script>