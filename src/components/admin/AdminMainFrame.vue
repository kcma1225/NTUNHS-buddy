<template>
    <div class="flex flex-col min-h-screen">
      <AdminHeader @switch-component="switchComponent" />
  
      <main class="flex-grow p-4 bg-gray-100">
        <component :is="currentComponent" />
      </main>
    </div>
  </template>
  
  <script>
  import AdminHeader from "./AdminHeader.vue";
  import StudentManagement from "./StudentManagement.vue";
  import CourseManagement from "./CourseManagement.vue";
  
  export default {
    name: "AdminMainFrame",
    components: {
      AdminHeader,
      StudentManagement,
      CourseManagement,
    },
    data() {
      return {
        currentComponent: "StudentManagement", // 預設顯示學生管理
      };
    },
    methods: {
      switchComponent(componentName) {
        if (componentName === "student-management") {
          this.currentComponent = "StudentManagement";
        } else if (componentName === "course-management") {
          this.currentComponent = "CourseManagement";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 根據需要添加樣式 */
  </style>
  