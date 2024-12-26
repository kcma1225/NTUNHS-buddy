<template>
    <div class="flex flex-col min-h-screen">
      <AdminHeader @switch-component="switchComponent" />
  
      <main class="flex-grow p-4 bg-gray-100">
        <component :is="currentComponent" />
      </main>
    </div>
  </template>
  
  <script>
  import StudentHeader from "./StudentHeader.vue";
  import FavoriteCourse from "./FavoriteCourse.vue";
  import MockCourse from "./MockCourse.vue";

  export default {
    name: "AdminMainFrame",
    components: {
      StudentHeader,
      FavoriteCourse,
      MockCourse,
    },
    data() {
      return {
        currentComponent: "FavoriteCourse", // 預設顯示學生管理
      };
    },
    methods: {
      switchComponent(componentName) {
        if (componentName === "favorite-course") {
          this.currentComponent = "FavoriteCourse";
        } else if (componentName === "mock-course") {
          this.currentComponent = "MockCourse";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 根據需要添加樣式 */
  </style>
  