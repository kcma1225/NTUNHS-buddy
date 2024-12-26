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
        class="h-11 md:h-10 lg:h-12 transition-all duration-300"
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
          class="absolute top-full left-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg opacity-100 transition duration-300 z-50 p-0 m-0 list-none"
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
        class="text-white text-base cursor-pointer no-underline hover:underline underline-offset-4 decoration-solid decoration-2 decoration-slate-200 transition duration-300"
      >
        最新消息
      </a>

      <!-- 幫助中心 -->
      <a
        href="https://example.com"
        target="_blank"
        rel="noopener noreferrer"
        class="text-white text-base cursor-pointer no-underline hover:underline underline-offset-4 decoration-solid decoration-2 decoration-slate-200 transition duration-300"
      >
        幫助中心
      </a>

      <!-- 登入/已登入狀態 -->
      <a
        v-if="!isAuthenticated"
        @click="$emit('open-login')"
        class="flex items-center text-white text-base cursor-pointer no-underline hover:text-opacity-80 transition duration-300"
      >
        <i class="bi bi-person mr-1"></i> 登入
      </a>
      <div
        v-else
        class="relative flex items-center text-white text-base cursor-pointer no-underline hover:text-opacity-80 transition duration-300"
        @click="togglePopup"
      >
        <i class="bi bi-person-circle mr-1"></i> {{ cookiesData.name || "admin" }}
        <div
          v-if="isPopupVisible"
          class="absolute top-full right-0 mt-2 w-48 bg-white border border-gray-300 rounded-lg shadow-lg z-50 p-2"
        >
          <div v-if="cookiesData.role === 'admin'">
            <a
              href="/admin"
              class="block p-2 text-black no-underline hover:bg-gray-100 rounded"
            >
              管理員設定介面
            </a>
            <button
              @click="logout"
              class="block w-full text-left p-2 text-red-500 no-underline hover:bg-red-100 rounded"
            >
              登出
            </button>
          </div>
          <div v-else-if="cookiesData.role === 'student'">
            <!-- <a
              href="/profile"
              class="block p-2 text-black no-underline hover:bg-gray-100 rounded"
            >
              個人資料設定
            </a> -->
            <a
              href="/student"
              class="block p-2 text-black no-underline hover:bg-gray-100 rounded"
            >
              收藏課程
            </a>
            <!-- <a
              href="/schedule"
              class="block p-2 text-black no-underline hover:bg-gray-100 rounded"
            >
              模擬排課
            </a> -->
            <button
              @click="logout"
              class="block w-full text-left p-2 text-red-500 no-underline hover:bg-red-100 rounded"
            >
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 點擊空白區域關閉彈出視窗 -->
    <div
      v-if="isPopupVisible"
      class="fixed inset-0 bg-transparent"
      @click="closePopup"
    ></div>
  </header>
</template>

<script>
import Cookies from "js-cookie";

export default {
  data() {
    return {
      logoSrc: new URL("../../assets/images/logo-white-text.png", import.meta.url).href,
      isMobileMenuOpen: false,
      activeDropdown: null,
      activeSubMenu: null,
      dropdowns: [
        { title: "相關連結", items: [{ name: "113-1選課行事曆", link: "#" }] },
        { title: "退選課程", items: [{ name: "停修申請填寫說明", link: "#" }] },
        { title: "下載專區", items: [{ name: "紙本退課單", link: "#" }] },
      ],
      cookiesData: this.getCookiesData(),
      isAuthenticated: this.checkAuthentication(),
      isPopupVisible: false,
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
      }, 300);
    },
    cancelCloseDropdown() {
      clearTimeout(this.closeTimeout);
    },
    getCookiesData() {
      return {
        name: Cookies.get("name"),
        username: Cookies.get("username"),
        role: Cookies.get("role"),
        token: Cookies.get("auth_token"),
      };
    },checkAuthentication() {
      const token = Cookies.get("auth_token");
      return !!token;
    },
    togglePopup() {
      this.isPopupVisible = !this.isPopupVisible;
    },
    closePopup() {
      this.isPopupVisible = false;
    },
    logout() {
      Cookies.remove("name");
      Cookies.remove("username");
      Cookies.remove("role");
      Cookies.remove("auth_token");
      this.isPopupVisible = false;
      location.reload();
    },
  },
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
