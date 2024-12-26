<template>
    <header class="bg-green-900 text-white flex items-center justify-between px-4 py-3 shadow-md">
      <!-- Logo and Back Icon -->
      <div class="flex items-center space-x-2">
        <i class="bi bi-arrow-return-left text-xl cursor-pointer" @click="goToRoot"></i>
        <span class="font-bold text-xl cursor-pointer" @click="goToRoot">課程查詢系統 <b>Student</b></span>
      </div>
  
      <!-- Navigation Links -->
      <nav class="hidden md:flex space-x-4">
        <a @click="switchComponent('favorite-course')" class="hover:text-gray-300 cursor-pointer">收藏課程</a>
        <a @click="switchComponent('mock-course')" class="hover:text-gray-300 cursor-pointer">模擬排課</a>
      </nav>
  
      <!-- Mobile Menu Button -->
      <button class="md:hidden text-white text-2xl" @click="toggleMobileMenu">☰</button>
  
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="absolute top-12 left-0 w-full bg-green-800 text-white shadow-lg md:hidden">
        <ul class="space-y-2 py-4 px-6">
          <li><a @click="switchComponent('favorite-course')" class="block hover:text-gray-300 cursor-pointer">收藏課程</a></li>
          <li><a @click="switchComponent('mock-course')" class="block hover:text-gray-300 cursor-pointer">模擬排課</a></li>
        </ul>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    data() {
      return {
        logoSrc: new URL("../../assets/images/logo-white-text.png", import.meta.url).href,
        mobileMenuOpen: false,
      };
    },
    methods: {
      toggleMobileMenu() {
        this.mobileMenuOpen = !this.mobileMenuOpen;
      },
      goToRoot() {
        this.$router.push("/");
      },
      switchComponent(componentName) {
        this.$emit("switch-component", componentName);
      },
    },
  };
  </script>
  
  <style scoped>
  header a {
    text-decoration: none;
    color: inherit;
  }
  header a:hover {
    color: #d1d5db; /* Tailwind gray-300 */
  }
  .bi {
    margin-right: 0.5rem;
  }
  </style>
  