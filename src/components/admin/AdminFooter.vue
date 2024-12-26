<!-- AdminFooter.vue -->
<template>
    <footer class="bg-white text-gray-700 text-sm py-2 shadow-inner">
      <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <!-- Left Side -->
        <div class="text-center md:text-left">
          <p class="font-light text-lg">北護課程查詢系統 - 管理員專區</p>
          <p class="text-xs text-gray-500">Copyright © 2024 系統分析與設計 - 第五組 v1.0</p>
        </div>
  
        <!-- Right Side -->
        <div class="flex space-x-4 text-xs md:text-sm">
          <a href="https://www.ntunhs.edu.tw/" class="hover:text-gray-600">國立臺北護理健康大學</a>
          <span class="hidden md:inline">|</span>
          <a href="https://academic.ntunhs.edu.tw/" class="hover:text-gray-600">教務處首頁</a>
          <span class="hidden md:inline">|</span>
          <a href="https://example.com" class="hover:text-gray-600">用戶協議</a>
          <span class="hidden md:inline">|</span>
          <a href="https://example.com" class="hover:text-gray-600">隱私權保護政策</a>
        </div>
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: "AdminFooter",
  };
  </script>
  
  <style scoped>
  a {
    text-decoration: none;
    color: inherit;
  }
  a:hover {
    color: #4b5563; /* Tailwind gray-600 */
  }
  </style>
  