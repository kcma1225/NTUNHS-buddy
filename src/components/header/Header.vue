<template>
  <header class="header" ref="header">
    <a href="/" class="logo-link">
      <img :src="logoSrc" alt="Logo" class="logo" />
    </a>
    <nav class="nav">
      <ul :class="{ mobile: isMobileMenuOpen }">
        <li v-if="!isMobileMenuOpen">
          <a @click="$emit('open-news')" class="menu-item">最新消息</a>
        </li>
        <li v-if="isMobileMenuOpen">
          <a @click="$emit('open-login')" class="menu-item">登入</a>
        </li>
        <li v-if="isMobileMenuOpen">
          <a @click="$emit('open-news')" class="menu-item">最新消息</a>
        </li>
        <li>
          <!-- 幫助中心：在新分頁開啟 -->
          <a href="https://example.com" target="_blank" rel="noopener noreferrer">
            幫助中心
          </a>
        </li>
        <li>
          <a href="#">ENGLISH</a>
        </li>
        <li v-if="!isMobileMenuOpen">
          <a @click="$emit('open-login')" class="menu-item">登入</a>
        </li>
      </ul>
      <button class="menu-toggle" @click="toggleMobileMenu">☰</button>
    </nav>
  </header>
</template>

<script>
import "../../assets/css/Header.css";
export default {
  props: ["isLoginVisible", "isNewsVisible"],
  data() {
    return {
      logoWhite: new URL("../../assets/images/logo-white-text.png", import.meta.url).href,
      isMobileMenuOpen: false,
    };
  },
  created() {
    this.logoSrc = this.logoWhite;
  },
  mounted() {
    // 全局點擊事件
    document.addEventListener("click", this.handleClickOutside);
  },
  destroyed() {
    // 移除全局事件監聽
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    handleClickOutside(event) {
      const header = this.$refs.header;
      if (header && !header.contains(event.target)) {
        // 點擊 header 以外的地方時關閉選單
        this.isMobileMenuOpen = false;
      }
    },
  },
};
</script>
