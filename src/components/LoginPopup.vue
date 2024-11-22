<template>
    <div class="login-popup">
      <div class="popup-content">
        <!-- 上方區塊 -->
        <div class="popup-header">
          <button @click="$emit('close-login')" class="close-button">✖</button>
          <div class="popup-logo-container">
            <img src="../assets/images/logo-black-text.png" alt="Logo" class="popup-logo" />
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
  
  <style scoped>
  .login-popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  .popup-content {
    background-color: white;
    width: 90%;
    max-width: 400px;
    border-radius: 8px;
    overflow: hidden;
    padding: 0;
  }
  .popup-header {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 20px;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
    position: relative;
  }
  .close-button {
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    background: none;
    border: none;
    font-size: 20px;
    color: black;
    cursor: pointer;
  }
  .popup-logo-container {
    text-align: center;
  }
  .popup-logo {
    width: 200px;
  }
  .popup-title {
    text-align: center;
    margin: 20px 0;
    font-size: 22px;
    font-weight: bold;
    color: black;
  }
  .popup-body {
    padding: 20px;
  }
  .form-group {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0 20px;
  }
  form label {
    font-size: 14px;
    color: black;
    margin-bottom: 5px;
  }
  form input {
    width: 100%;
    max-width: 360px;
    margin: 0 auto;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;
    color: black;
  }
  form input::placeholder {
    color: gray;
  }
  .error-message {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }
  .forgot-password {
    display: block;
    margin: 10px auto;
    background: none;
    border: none;
    color: #009944;
    text-align: center;
    cursor: pointer;
  }
  .login-submit {
    background-color: #009944;
    color: white;
    border: none;
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
    margin: 0 auto;
    display: block;
  }
  </style>
  