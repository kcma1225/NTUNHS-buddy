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
            <button @click="removeCourse(course._id)" 
                    class="mt-2 px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 text-sm">
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
                <div v-if="getCourseAt(period.id, getWeekDayNumber(day))" 
                     class="absolute inset-0 m-1 p-2 bg-blue-100 rounded shadow-sm">
                  <div class="text-sm font-medium text-blue-900">
                    {{ getCourseAt(period.id, getWeekDayNumber(day)).課程名稱 }}
                  </div>
                  <div class="text-xs text-blue-700">
                    {{ getCourseAt(period.id, getWeekDayNumber(day)).教師姓名.split('\n')[0] }}
                  </div>
                  <div class="text-xs text-blue-600">
                    {{ getCourseAt(period.id, getWeekDayNumber(day)).地點 }}
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
    };
  },
  computed: {
    getSelectedCourses() {
      const savedCourses = localStorage.getItem('selectedCourses');
      return savedCourses ? JSON.parse(savedCourses) : [];
    }
  },
  methods: {
    getWeekDayNumber(day) {
      return (this.weekDays.indexOf(day) + 1).toString();
    },

    // 取得特定時間點的課程
    getCourseAt(periodId, day) {
      return this.getSelectedCourses.find(course => 
        course.星期 === day && 
        course.節次.split(',').includes(periodId.toString())
      );
    },

    // 檢查時間衝突
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

    // 新增課程
    addToSchedule(course) {
      // 檢查時間衝突
      if (this.checkTimeConflict(course)) {
        alert('課程時間衝突！無法加入此課程。');
        return;
      }

      // 取得現有課程
      const currentCourses = this.getSelectedCourses;
      
      // 檢查課程是否已存在
      if (currentCourses.some(c => c._id === course._id)) {
        alert('此課程已經加入！');
        return;
      }

      // 新增課程
      currentCourses.push(course);
      localStorage.setItem('selectedCourses', JSON.stringify(currentCourses));
      alert('成功加入課程！');
    },

    // 移除課程
    removeCourse(courseId) {
      const currentCourses = this.getSelectedCourses;
      const updatedCourses = currentCourses.filter(course => course._id !== courseId);
      localStorage.setItem('selectedCourses', JSON.stringify(updatedCourses));
    }
  }
};
</script>

<style scoped>
.min-h-[80px] {
  min-height: 80px;
}
</style>