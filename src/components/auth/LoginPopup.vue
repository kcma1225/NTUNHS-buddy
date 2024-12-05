<template>
    <div class="login-popup">
      <div class="popup-content">
        <!-- 上方區塊 -->
        <div class="popup-header">
          <button @click="$emit('close-login')" class="close-button">✖</button>
          <div class="popup-logo-container">
            <img src="../../assets/images/logo-black-text.png" alt="Logo" class="popup-logo" />
          </div>
        </div>
        <h2 class="popup-title">登入</h2>
        <!-- 下方區塊 -->
        <div class="popup-body">
          <form @submit.prevent="validateForm">
            <div class="form-group">
              <label for="username">帳號：</label>
              <input
                type="text"
                id="username"
                v-model="username"
                placeholder="輸入帳號"
              />
              <p v-if="errors.username" class="error-message">{{ errors.username }}</p>
            </div>
            <div class="form-group">
              <label for="password">密碼：</label>
              <input
                type="password"
                id="password"
                v-model="password"
                placeholder="輸入密碼"
              />
              <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
            </div>
            <button type="button" class="forgot-password">忘記密碼</button>
            <button type="submit" class="login-submit">登入</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import '../../assets/css/LoginPopup.css';
  export default {
    data() {
      return {
        username: "",
        password: "",
        errors: {
          username: null,
          password: null,
        },
      };
    },
    methods: {
      validateForm() {
        this.errors.username = this.username.trim() === "" ? "請輸入帳號" : null;
        this.errors.password = this.password.trim() === "" ? "請輸入密碼" : null;
  
        if (!this.errors.username && !this.errors.password) {
          alert("登入成功！");
          // 這裡可以觸發 API 請求或其他邏輯
        }
      },
    },
  };
  </script>
  
  