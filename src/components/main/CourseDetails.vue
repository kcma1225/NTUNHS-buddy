<template>
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center p-4 z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl">
      <!-- Close Button -->
      <button
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors duration-200"
        @click="$emit('close')"
      >
        <i class="bi bi-x-circle-fill text-2xl"></i>
      </button>

      <!-- Course Name Section -->
      <div class="p-8 border-b border-gray-100">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">{{ course.課程名稱 }}</h2>
        <div class="text-lg text-gray-500">{{ course.科目代號 }}</div>
      </div>

      <!-- Teacher Section -->
      <div class="px-8 py-6 bg-gray-50 border-b border-gray-100">
        <div class="flex items-center gap-3 mb-2">
          <i class="bi bi-person-fill text-2xl text-green-600"></i>
          <h3 class="text-xl font-semibold text-gray-700">授課教師</h3>
        </div>
        <p class="text-lg text-gray-600 pl-9">{{ processedTeachers(course.教師姓名) }}</p>
      </div>

      <!-- Other Details Section -->
      <div class="p-8 space-y-4">
        <div class="grid grid-cols-2 gap-6">
          <!-- Basic Course Info -->
          <div class="space-y-4">
            <div class="flex items-center gap-2">
              <i class="bi bi-mortarboard-fill text-blue-500"></i>
              <span class="text-gray-600">{{ course.年級 }}年級</span>
            </div>
            
            <div class="flex items-center gap-2">
              <i class="bi bi-calendar3 text-purple-500"></i>
              <span class="text-gray-600">{{ course.學期 }}</span>
            </div>

            <div class="flex items-center gap-2">
              <i class="bi bi-people-fill text-red-500"></i>
              <span class="text-gray-600">{{ course.上課人數 }}人</span>
            </div>
          </div>

          <!-- Time and Location -->
          <div class="space-y-4">
            <div class="flex items-center gap-2">
              <i class="bi bi-geo-alt-fill text-orange-500"></i>
              <span class="text-gray-600">{{ course.地點 }}</span>
            </div>

            <div class="flex items-center gap-2">
              <i class="bi bi-clock-fill text-green-500"></i>
              <span class="text-gray-600">
                星期{{ course.星期 }} | {{ formatPeriod(course.節次) }}節
              </span>
            </div>
          </div>
        </div>

        <!-- Course Category -->
        <div class="pt-4 border-t border-gray-100">
          <div class="flex items-center gap-2 text-gray-700">
            <i class="bi bi-bookmark-fill text-indigo-500"></i>
            <span class="font-medium">課程內容分類：</span>
            <span class="text-gray-600">{{ course.課程內容分類 }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatPeriod(periodString) {
      const periods = periodString.split(",").map((p) => parseInt(p, 10));
      return `${Math.min(...periods)}-${Math.max(...periods)}`;
    },
    processedTeachers(teacherString) {
      const rawTeachers = teacherString.split("\n")[0];
      const teachers = rawTeachers
        .split(",")
        .filter((name) => name.trim() !== "")
        .map((name) => name.trim());
      return teachers.length > 0 ? teachers.join(", ") : "查無資料";
    },
  },
};
</script>

<style scoped>
</style>