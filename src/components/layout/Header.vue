<template>
  <header class="header">
    <a href="/" class="logo-link">
      <img :src="logoSrc" alt="Logo" class="logo" />
    </a>
    <nav class="nav">
      <ul :class="{ mobile: isMobileMenuOpen }">
        <li v-if="isMobileMenuOpen">
          <a @click="$emit('open-login')" class="menu-item">登入</a>
        </li>
        <li v-if="isMobileMenuOpen">
          <a @click="$emit('open-news')" class="menu-item">最新消息</a>
        </li>
        <li v-if="!isMobileMenuOpen">
          <a @click="$emit('open-news')" class="menu-item">最新消息</a>
        </li>
        <li>
          <a href="#">幫助中心</a>
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
import '../../assets/css/Header.css';
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
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
  },
};
</script>


