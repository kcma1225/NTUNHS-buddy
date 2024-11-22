<template>
  <header class="header">
    <a href="/" class="logo-link">
      <img :src="logoSrc" alt="Logo" class="logo" />
    </a>
    <nav class="nav">
      <ul :class="{ mobile: isMobileMenuOpen }">
        <li v-if="isMobileMenuOpen"><a @click="$emit('open-login')" class="menu-item">登入</a></li>
        <li><a href="#">最新消息</a></li>
        <li><a href="#">幫助中心</a></li>
        <li><a href="#">ENGLISH</a></li>
        <li v-if="!isMobileMenuOpen"><a @click="$emit('open-login')" class="menu-item">登入</a></li>
      </ul>
      <button class="menu-toggle" @click="toggleMobileMenu">☰</button>
    </nav>
  </header>
</template>

<script>
export default {
  props: ['isLoginVisible'],
  data() {
    return {
      logoWhite: new URL('../assets/images/logo-white-text.png', import.meta.url).href,
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

<style scoped>
.header {
  background-color: #003618;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}
.logo {
  height: 50px;
}
.nav ul {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0 50px; /* 加入 padding 確保內距 */
  flex-wrap: nowrap;
  overflow: hidden;
}
.nav ul.mobile {
  flex-direction: column;
  background-color: #003618;
  position: absolute;
  top: 60px;
  left: 0;
  width: 100%;
}
.nav ul.mobile li {
  margin: 10px 0;
}
.nav ul li {
  margin-left: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.nav a,
.menu-item {
  color: white;
  text-decoration: none;
  font-size: 16px;
  cursor: pointer;
  white-space: nowrap;
}
.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

/* 響應式樣式 */
@media (max-width: 768px) {
  .nav ul {
    display: none;
  }
  .nav ul.mobile {
    display: flex;
  }
  .menu-toggle {
    display: block;
  }
}
</style>
