<template>
  <header
    class="bg-green-900 flex items-center justify-between p-2 fixed top-0 left-0 w-full z-50 shadow-lg"
    ref="header"
  >
    <!-- 漢堡按鈕 (手機版) -->
    <button
      class="md:hidden text-white text-2xl cursor-pointer p-2"
      @click="toggleMobileMenu"
    >
      ☰
    </button>

    <!-- Logo -->
    <a
      href="/"
      class="flex items-center justify-center flex-shrink-0 md:justify-start md:ml-4"
      :class="{ 'absolute left-1/2 transform -translate-x-1/2': isMobile }"
    >
      <img
        :src="logoSrc"
        alt="Logo"
        class="h-12 md:h-10 lg:h-12 transition-all duration-300"
      />
    </a>

    

    <!-- 手機版 Person Icon -->
    <button
      class="md:hidden text-white text-2xl p-2 mr-4"
      @click="$emit('open-login')"
    >
      <i class="bi bi-person"></i>
    </button>

    <!-- Dropdown Menus (桌面版，中間偏左) -->
    <nav class="hidden md:flex flex-1 justify-start space-x-8 ml-16">
      <div
        v-for="(dropdown, index) in dropdowns"
        :key="index"
        class="relative group"
        @mouseenter="openDropdown(index)"
        @mouseleave="delayCloseDropdown"
      >
        <a
          href="#"
          class="text-white text-base cursor-pointer no-underline flex items-center hover:text-opacity-80 transition duration-300"
        >
          {{ dropdown.title }}
          <svg
            class="w-3 h-3 ml-1 transition-transform duration-300"
            :class="{ 'rotate-180': activeDropdown === index }"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 12 12"
          >
            <path d="M10 2.586 11.414 4 6 9.414.586 4 2 2.586l4 4z" fill="white" />
          </svg>
        </a>
        <ul
          v-show="activeDropdown === index"
          @mouseenter="cancelCloseDropdown"
          @mouseleave="delayCloseDropdown"
          class="absolute top-full left-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg opacity-100 transition duration-300 z-50 p-0 m-0 list-none "
        >
          <li
            v-for="(item, idx) in dropdown.items"
            :key="idx"
            class="hover:bg-gray-100 cursor-pointer"
          >
            <a
              :href="item.link"
              target="_blank"
              class="block w-full p-2 text-gray-800 no-underline hover:text-indigo-500 transition duration-300"
            >
              {{ item.name }}
            </a>
          </li>
        </ul>
      </div>
    </nav>

<!-- Header Navigation Links -->
<nav class="hidden md:flex items-center space-x-8 mr-8">
      <!-- 最新消息 -->
      <a
        @click="$emit('open-news')"
        class="text-white text-base cursor-pointer no-underline hover:text-opacity-80 transition duration-300"
      >
        最新消息
      </a>

      <!-- 幫助中心 -->
      <a
        href="https://example.com"
        target="_blank"
        rel="noopener noreferrer"
        class="text-white text-base cursor-pointer no-underline hover:text-opacity-80 transition duration-300"
      >
        幫助中心
      </a>

      <!-- Person Icon + 登入 -->
      <a
        @click="$emit('open-login')"
        class="flex items-center text-white text-base cursor-pointer no-underline hover:text-opacity-80 transition duration-300"
      >
        <i class="bi bi-person mr-1"></i> 登入
      </a>
    </nav>

    <!-- 手機版菜單 (遮罩區域 + Menu 本體) -->
    <div
      v-if="isMobileMenuOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40"
      @click="closeMobileMenu"
    >
      <!-- Menu 本體 -->
      <div
        class="h-full w-2/3 bg-white text-black shadow-lg transform transition-transform duration-500"
        @click.stop
      >
        <ul class="list-none p-6 space-y-4 h-full flex flex-col justify-between">
          <!-- Dropdown 項目 -->
          <li v-for="(dropdown, index) in dropdowns" :key="index">
            <div @click="toggleSubMenu(index)">
              <div class="flex justify-between items-center cursor-pointer p-2 no-underline">
                <span>{{ dropdown.title }}</span>
                <svg
                  class="w-4 h-4 transition-transform duration-300"
                  :class="{ 'rotate-180': activeSubMenu === index }"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 12 12"
                >
                  <path d="M10 2.586 11.414 4 6 9.414.586 4 2 2.586l4 4z" />
                </svg>
              </div>
              <ul v-show="activeSubMenu === index" class="pl-4 space-y-2">
                <li
                  v-for="(item, idx) in dropdown.items"
                  :key="idx"
                  class="hover:text-indigo-500"
                >
                  <a :href="item.link">{{ item.name }}</a>
                </li>
              </ul>
            </div>
          </li>
          <!-- 底部資訊 -->
          <div class="mt-auto text-center text-gray-600">
            <a @click="$emit('open-news')" class="flex mb-2">最新消息</a>
            <a href="https://example.com" class="flex mb-2">幫助中心</a>
            <div class="inline-flex text-xs text-gray-400">課程查詢系統 v1.0</div>
          </div>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      logoSrc: new URL("../../assets/images/logo-white-text.png", import.meta.url).href,
      isMobileMenuOpen: false,
      activeDropdown: null,
      activeSubMenu: null,
      dropdowns: [
        { title: "相關連結", items: [{ name: "113-1選課行事曆", link: "https://teaching-acad.ntunhs.edu.tw/var/file/40/1040/attach/30/pta_57433_1288895_68818.pdf" }, { name: "校際選課", link: "#" }, { name: "課程抵免", link: "#" }, { name: "修課", link: "#" }] },
        { title: "退選課程", items: [{ name: "停修申請填寫說明", link: "#" }, { name: "線上退課", link: "#" }] },
        { title: "下載專區", items: [{ name: "紙本退課單", link: "#" }, { name: "英文畢業門檻申請表", link: "#" }, { name: "學分抵免申請表", link: "#" }, { name: "英文免修申請表", link: "#" }, { name: "大學部修讀研究所課程申請書", link: "#" }] },
        { title: "常見問題", items: [{ name: "帳號登入問題", link: "#" }, { name: "課程查詢與篩選", link: "#" }, { name: "課程限制與先修條件", link: "#" }, { name: "學期相關規定", link: "#" }, { name: "系統錯誤與技術支援", link: "#" }] },
      ],
    };
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    },
    toggleSubMenu(index) {
      this.activeSubMenu = this.activeSubMenu === index ? null : index;
    },
    openDropdown(index) {
      this.cancelCloseDropdown();
      this.activeDropdown = index;
    },
    delayCloseDropdown() {
      this.closeTimeout = setTimeout(() => {
        this.activeDropdown = null;
      }, 300); // 延遲 300ms
    },
    cancelCloseDropdown() {
      clearTimeout(this.closeTimeout);
    },
  },
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
