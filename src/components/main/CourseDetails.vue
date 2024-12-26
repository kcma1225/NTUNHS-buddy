<template>
    <div
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
      @click.self="$emit('close')"
    >
      <div class="bg-white rounded-lg shadow-lg w-3/4 max-w-2xl p-6 relative">
        <button
          class="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
          @click="$emit('close')"
        >
          <i class="bi bi-x-circle-fill text-2xl"></i>
        </button>
  
        <h2 class="text-2xl font-bold text-green-800 mb-4">{{ course.課程名稱 }}</h2>
  
        <div class="text-sm text-gray-700">
          <p><strong>課程名稱:</strong> {{ course.課程名稱 }}</p>
          <p><strong>年級:</strong> {{ course.年級 }}年級</p>
          <p><strong>學期:</strong> {{ course.學期 }}</p>
          <p><strong>科目代號:</strong> {{ course.科目代號 }}</p>
          <p><strong>教師姓名:</strong> {{ processedTeachers(course.教師姓名) }}</p>
          <p><strong>上課人數:</strong> {{ course.上課人數 }}人</p>
          <p><strong>地點:</strong> {{ course.地點 }}</p>
          <p><strong>時間:</strong> 星期{{ course.星期 }} | {{ formatPeriod(course.節次) }}節</p>
          <p><strong>課程內容分類:</strong> {{ course.課程內容分類 }}</p>
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