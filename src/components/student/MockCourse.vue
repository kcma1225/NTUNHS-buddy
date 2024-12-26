<template>
  <div class="max-w-full p-6">
    <h1 class="text-2xl font-bold mb-6">模擬排課</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- 課程列表區域 -->
      <div class="lg:col-span-1 bg-white rounded-lg shadow-md p-4">
        <h2 class="text-lg font-semibold mb-4">已選課程</h2>
        <div class="space-y-3">
          <div v-for="course in getSelectedCourses" :key="course._id" 
               class="p-3 bg-blue-50 rounded-md border border-blue-200">
            <h3 class="font-medium text-blue-900">{{ course.課程名稱 }}</h3>
            <p class="text-sm text-blue-700">{{ course.教師姓名.split('\n')[0] }}</p>
            <p class="text-sm text-blue-600">星期{{ course.星期 }} {{ course.節次.replace(/,/g, ',') }}節</p>
            <p class="text-sm text-blue-600">地點: {{ course.地點 }}</p>
            <button @click="handleRemoveCourse(course._id)" 
                    class="mt-2 px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 text-sm flex items-center gap-2">
              <i class="bi bi-trash"></i>
              刪除課程
            </button>
          </div>
        </div>
      </div>

      <!-- 課程時間表格區域 -->
      <div class="lg:col-span-3 bg-white rounded-lg shadow-md overflow-auto">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-50">
              <th class="border p-2 min-w-[100px]">節次 / 時間</th>
              <th v-for="day in weekDays" :key="day" class="border p-2 min-w-[130px]">
                {{ day }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(period, index) in periods" :key="period.id">
              <td class="border p-2 bg-gray-50">
                <div class="text-sm font-medium">第 {{ period.id }} 節</div>
                <div class="text-xs text-gray-600">{{ period.time }}</div>
              </td>
              <td v-for="day in weekDays" :key="`${period.id}-${day}`" 
                  class="border p-2 relative min-h-[80px]">
                <button v-if="getCourseAt(period.id, getWeekDayNumber(day))"
                        @click="showCourseDetail(getCourseAt(period.id, getWeekDayNumber(day)))"
                        class="absolute inset-0 m-1 p-2 bg-blue-100 hover:bg-blue-200 rounded shadow-sm 
                               transition-colors duration-200 text-left overflow-hidden">
                  <div class="text-sm font-medium text-blue-900 truncate">
                    {{ getCourseAt(period.id, getWeekDayNumber(day)).課程名稱 }}
                  </div>
                  <div class="text-xs text-blue-700 truncate">
                    {{ getCourseAt(period.id, getWeekDayNumber(day)).地點 }}
                  </div>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 整合的 CourseDetail 組件 -->
    <div v-if="selectedCourse" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
         @click="closeDetail">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4"
           @click.stop>
        <!-- 標題區塊 -->
        <div class="bg-gradient-to-r from-green-700 to-green-900 text-white px-6 py-4 rounded-t-2xl flex items-center justify-between">
          <h3 class="text-xl font-bold">課程詳情</h3>
          <button @click="closeDetail" 
                  class="text-white hover:text-green-200 transition-colors">
            <i class="bi bi-x-lg text-xl"></i>
          </button>
        </div>

        <!-- 詳情內容 -->
        <div class="p-6 space-y-6">
          <div class="space-y-4">
            <h4 class="text-2xl font-bold text-gray-800">{{ selectedCourse.課程名稱 }}</h4>
            
            <!-- 基本資訊 -->
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-bookmark mr-2"></i>
                  編號：{{ selectedCourse.編號 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-calendar3 mr-2"></i>
                  學期：{{ selectedCourse.學期 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-building mr-2"></i>
                  系所：{{ selectedCourse.系所 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-mortarboard mr-2"></i>
                  年級：{{ selectedCourse.年級 }}年級
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-people mr-2"></i>
                  班組：{{ selectedCourse.班組 }}
                </p>
              </div>
              <div class="space-y-2">
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-hash mr-2"></i>
                  科目代號：{{ selectedCourse.科目代號 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-book mr-2"></i>
                  學分數：{{ selectedCourse.學分數 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-journal-text mr-2"></i>
                  課別：{{ selectedCourse.課別 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-person-badge mr-2"></i>
                  上課人數：{{ selectedCourse.上課人數 }}
                </p>
                <p class="flex items-center text-gray-600">
                  <i class="bi bi-tags mr-2"></i>
                  課程內容分類：{{ selectedCourse.課程內容分類 }}
                </p>
              </div>
            </div>

            <!-- 上課資訊 -->
            <div class="border-t pt-4">
              <h5 class="font-semibold text-gray-700 mb-3">上課資訊</h5>
              <div class="grid grid-cols-2 gap-4">
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-geo-alt mr-2"></i>
                  地點：{{ selectedCourse.地點 }}
                </div>
                <div class="flex items-center text-gray-600">
                  <i class="bi bi-clock mr-2"></i>
                  時間：星期{{ selectedCourse.星期 }} | {{ selectedCourse.節次 }}節
                </div>
              </div>
            </div>

            <!-- 教師資訊 -->
            <div class="border-t pt-4">
              <h5 class="font-semibold text-gray-700 mb-3">授課教師</h5>
              <div class="flex flex-wrap gap-2">
                <template v-if="isValidTeachers(selectedCourse.教師姓名)">
                  <span v-for="teacher in processedTeachers(selectedCourse.教師姓名)"
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
  </div>
</template>

<script>
export default {
  name: "MockCourse",
  data() {
    return {
      weekDays: ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'],
      periods: [
        { id: 1, time: '08:10~09:00' },
        { id: 2, time: '09:10~10:00' },
        { id: 3, time: '10:10~11:00' },
        { id: 4, time: '11:10~12:00' },
        { id: 5, time: '12:40~13:30' },
        { id: 6, time: '13:40~14:30' },
        { id: 7, time: '14:40~15:30' },
        { id: 8, time: '15:40~16:30' },
        { id: 9, time: '16:40~17:30' },
        { id: 10, time: '17:40~18:30' },
        { id: 11, time: '18:35~19:25' },
        { id: 12, time: '19:30~20:20' },
        { id: 13, time: '20:25~21:15' },
        { id: 14, time: '21:20~22:10' }
      ],
      selectedCourses: [],
      selectedCourse: null
    };
  },

  created() {
    this.loadCourses();
  },

  mounted() {
    window.addEventListener('keydown', this.handleEscKey);
  },

  beforeDestroy() {
    window.removeEventListener('keydown', this.handleEscKey);
  },

  computed: {
    getSelectedCourses() {
      const savedCourses = localStorage.getItem('selectedCourses');
      return savedCourses ? JSON.parse(savedCourses) : [];
    }
  },

  methods: {
    loadCourses() {
      const savedCourses = localStorage.getItem('selectedCourses');
      this.selectedCourses = savedCourses ? JSON.parse(savedCourses) : [];
    },
    
    getWeekDayNumber(day) {
      return (this.weekDays.indexOf(day) + 1).toString();
    },

    getCourseAt(periodId, day) {
      return this.getSelectedCourses.find(course => 
        course.星期 === day && 
        course.節次.split(',').includes(periodId.toString())
      );
    },

    checkTimeConflict(newCourse) {
      const existingCourses = this.getSelectedCourses;
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

    showCourseDetail(course) {
      this.selectedCourse = course;
    },

    closeDetail() {
      this.selectedCourse = null;
    },

    handleEscKey(e) {
      if (e.key === 'Escape' && this.selectedCourse) {
        this.closeDetail();
      }
    },

    handleRemoveCourse(courseId) {
      const currentCourses = this.getSelectedCourses;
      const updatedCourses = currentCourses.filter(course => course._id !== courseId);
      localStorage.setItem('selectedCourses', JSON.stringify(updatedCourses));
      window.location.reload();
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

    addToSchedule(course) {
      if (this.checkTimeConflict(course)) {
        alert('課程時間衝突！無法加入此課程。');
        return;
      }

      const currentCourses = this.getSelectedCourses;
      
      if (currentCourses.some(c => c._id === course._id)) {
        alert('此課程已經加入！');
        return;
      }

      currentCourses.push(course);
      localStorage.setItem('selectedCourses', JSON.stringify(currentCourses));
      alert('成功加入課程！');
    }
  }
};
</script>

<style scoped>
.min-h-[80px] {
  min-height: 80px;
}
</style>