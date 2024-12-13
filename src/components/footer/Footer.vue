<template>
    <footer class="bg-white text-gray-700 text-sm">
      <div
        class="container mx-auto py-3 px-4 flex flex-col md:flex-row justify-between items-center text-center md:text-left"
      >
        <!-- 左側 Main Title 和 Copyright -->
        <div class="flex flex-col items-center md:items-start mb-2 md:mb-0">
          <!-- Main Title -->
          <div class="text-lg font-light">北護課程查詢系統</div>
          <!-- Copyright -->
          <div class="text-xs text-gray-500 font-extralight mt-1">
            Copyright © 2024 系統分析與設計 - 第五組 v1.0
          </div>
        </div>
  
        <!-- 右側超連結，兩行並用 | 分隔 -->
        <div
          class="flex flex-col items-center md:items-end space-y-1 text-xs md:text-sm"
        >
          <!-- 第一行 -->
          <div class="flex space-x-2">
            <a
              href="https://www.ntunhs.edu.tw/"
              target="_blank"
              class="hover:text-gray-600 no-underline"
            >
              國立臺北護理健康大學
            </a>
            <span class="text-gray-400">|</span>
            <a
              href="https://academic.ntunhs.edu.tw/"
              target="_blank"
              class="hover:text-gray-600 no-underline"
            >
              教務處首頁
            </a>
          </div>
  
          <!-- 第二行 -->
          <div class="flex space-x-2">
            <a
              href="https://example.com"
              target="_blank"
              class="hover:text-gray-600 no-underline"
            >
              用戶協議
            </a>
            <span class="text-gray-400">|</span>
            <a
              href="https://example.com"
              target="_blank"
              class="hover:text-gray-600 no-underline"
            >
              隱私權保護政策
            </a>
          </div>
        </div>
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: "Footer",
  };
  </script>
  
  <style scoped>
  /* 基礎連結樣式 */
  a {
    text-decoration: none;
    color: inherit;
  }
  
  a:hover {
    color: #4b5563; /* Tailwind gray-600 */
  }
  </style>
  