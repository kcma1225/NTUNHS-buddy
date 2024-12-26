<template>
    <div id="admin-app" class="flex flex-col min-h-screen">
      <AdminHeader @logout="logout" @switch-component="switchComponent" />
  
      <main class="flex-grow pt-2">
        <div class="p-4 w-full">
          <component :is="currentComponent" />
        </div>
      </main>
  
      <AdminFooter />
    </div>
  </template>
  
  <script>
  import AdminHeader from "../components/admin/AdminHeader.vue";
  import AdminFooter from "../components/admin/AdminFooter.vue";
  import StudentManagement from "../components/admin/StudentManagement.vue";
  import CourseManagement from "../components/admin/CourseManagement.vue";
  
  export default {
    components: {
      AdminHeader,
      AdminFooter,
      StudentManagement,
      CourseManagement,
    },
    data() {
      return {
        currentComponent: "StudentManagement", // 預設顯示學生管理
      };
    },
    methods: {
      logout() {
        console.log("Admin logged out");
        // Perform logout logic
      },
      switchComponent(componentName) {
        if (componentName === "student-management") {
          this.currentComponent = "StudentManagement";
        } else if (componentName === "course-management") {
          this.currentComponent = "CourseManagement";
        }
      },
    },
    created() {
      console.log("Admin application initialized.");
    },
  };
  </script>
  
  <style scoped>
  .bg-dark-green {
    background-color: #2f4f4f;
  }
  </style>
