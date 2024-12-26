<template>
  <div class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white w-11/12 max-w-lg rounded-lg overflow-hidden">
      <!-- 上方區塊 -->
      <div class="flex justify-center items-center p-3 bg-gray-200 border-b border-gray-300 relative">
        <button @click="$emit('close-login')" class="absolute right-5 top-1/2 transform -translate-y-1/2 text-black text-xl cursor-pointer">
          ✖
        </button>
        <div>
          <img src="../../assets/images/logo-black-text.png" alt="Logo" class="w-60" />
        </div>
      </div>
      <h2 class="text-center mt-3 mb-2 text-xl font-bold text-black">登入</h2>
      <!-- 下方區塊 -->
      <div class="pt-3 pb-5 px-5">
        <form @submit.prevent="handleLogin">
          <div class="mb-3 flex flex-col">
            <label for="username" class="text-sm text-black mb-1">帳號：</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="輸入帳號"
              class="w-full p-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring focus:ring-green-500"
            />
            <p v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username }}</p>
          </div>
          <div class="mb-5 flex flex-col">
            <label for="password" class="text-sm text-black mb-1">密碼：</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="輸入密碼"
              class="w-full p-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring focus:ring-green-500"
            />
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
          </div>
          <button type="submit" class="block w-full bg-green-600 text-white p-2 text-center rounded hover:bg-green-700">
            登入
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import apiService from "../../api/apiService.js";

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
    async handleLogin() {
      // 驗證表單
      this.errors.username = this.username.trim() === "" ? "請輸入帳號" : null;
      this.errors.password = this.password.trim() === "" ? "請輸入密碼" : null;

      if (this.errors.username || this.errors.password) {
        return;
      }

      try {
        const response = await apiService.login({
          username: this.username.trim(),
          password: this.password.trim(),
        });

        const { role, username, name, token } = response.data;

        // 將資料存入 Cookies
        Cookies.set("role", role, { expires: 7 });
        Cookies.set("username", username, { expires: 7 });
        Cookies.set("name", name || "admin", { expires: 7 });
        Cookies.set("auth_token", token, { expires: 7 });

        // 成功通知框
        this.showAlert("success", "登入成功！");
        this.$emit("update-header", { role, username, name, token });

        // 重新整理頁面
        setTimeout(() => {
          location.reload();
        }, 1000);
      } catch (error) {
        console.error("Login failed:", error);
        // 失敗通知框
        this.showAlert("danger", "登入失敗，請檢查帳號和密碼");
      }
    },
    showAlert(type, message) {
      const alert = document.createElement("div");
      alert.className = `alert alert-${type} position-fixed top-0 end-0 mt-3 me-3 shadow-lg p-4 rounded-lg`;
      alert.style.zIndex = 1050;
      alert.style.width = "350px";
      alert.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
          <span>${message}</span>
          <button type="button" class="btn-close" aria-label="Close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
      `;

      document.body.appendChild(alert);

      setTimeout(() => {
        alert.remove();
      }, 3000);
    },
  },
};
</script>

<style scoped>
.alert {
  animation: fadeInOut 3s ease-in-out;
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
  }
  10%, 90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
