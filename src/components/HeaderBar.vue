<template>
  <nav class="header-bar">
    <div class="logo-container">
      <a href="/" class="logo-link">
        <img src="../assets/images/logo.png" alt="Logo" class="logo" />
      </a>
    </div>
    <ul class="nav-links">
      <li><a href="/latest-news">最新消息</a></li>
      <li><a href="/help-center">幫助中心</a></li>
      <li><a href="/english" class="highlight">English</a></li>
      <li class="login-button" @click="showLoginPopup">登入</li>
    </ul>
    <div v-if="isLoginPopupVisible" class="login-popup">
      <div class="login-content">
        <button class="close-button" @click="closeLoginPopup">✖</button>
        <div class="logo-container-popup">
          <img src="../assets/images/logo.png" alt="Logo" class="logo-popup" />
          <span class="title-popup">北護課程查詢系統</span>
        </div>
        <h2>登入：</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">帳號：</label>
            <input type="text" id="username" v-model="username" placeholder="輸入帳號" required />
          </div>
          <div class="form-group">
            <label for="password">密碼：</label>
            <input type="password" id="password" v-model="password" placeholder="輸入 密碼" required />
          </div>
          <div class="form-actions">
            <button type="button" class="forgot-password-button">忘記密碼</button>
            <button type="submit" class="login-submit-button">登入</button>
          </div>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'HeaderBar',
  data() {
    return {
      isLoginPopupVisible: false,
      username: '',
      password: '',
    };
  },
  methods: {
    showLoginPopup() {
      this.isLoginPopupVisible = true;
    },
    closeLoginPopup() {
      this.isLoginPopupVisible = false;
    },
    handleLogin() {
      // 處理登入邏輯
      console.log('登入中...', this.username, this.password);
      this.closeLoginPopup();
    },
  },
};
</script>

<style src="../assets/css/header-bar.css"></style>