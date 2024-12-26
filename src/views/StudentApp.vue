<template>
    <div id="student-app" class="flex flex-col min-h-screen">
      <StudentHeader @logout="logout" @switch-component="switchComponent" />
  
      <main class="flex-grow pt-2">
        <div class="p-4 w-full">
          <component :is="currentComponent" />
        </div>
      </main>
  
      <StudentFooter />
    </div>
  </template>
  
  <script>
  import StudentHeader from "../components/student/StudentHeader.vue";
  import StudentFooter from "../components/student/StudentFooter.vue";
  import FavoriteCourse from "../components/student/FavoriteCourse.vue";
  import MockCourse from "../components/student/MockCourse.vue";
  
  export default {
    components: {
      StudentHeader,
      StudentFooter,
      FavoriteCourse,
      MockCourse
    },
    data() {
      return {
        currentComponent: "FavoriteCourse", // 
      };
    },
    methods: {
      logout() {
        console.log("Student logged out");
        // Perform logout logic
      },
      switchComponent(componentName) {
        if (componentName === "favorite-course") {
          this.currentComponent = "FavoriteCourse";
        } else if (componentName === "mock-course") {
          this.currentComponent = "MockCourse";
        }
      },
    },
    created() {
      console.log("Student application initialized.");
    },
  };
  </script>
  
  <style scoped>
  .bg-light-blue {
    background-color: #e0f7fa;
  }
  </style>
