<template>
    <div class="max-w-2xl mx-auto p-6">
      <h1 class="text-2xl font-bold mb-6 text-gray-800">帳號設定</h1>
      
      <!-- 密碼修改卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700">修改密碼</h2>
        
        <form @submit.prevent="handlePasswordChange" class="space-y-4">
          <!-- 舊密碼輸入框 -->
          <div>
            <label for="oldPassword" class="block text-sm font-medium text-gray-700 mb-1">
              目前密碼
            </label>
            <input
              v-model="formData.oldPassword"
              type="password"
              id="oldPassword"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.oldPassword }"
              placeholder="請輸入目前密碼"
              required
            />
            <p v-if="errors.oldPassword" class="mt-1 text-sm text-red-600">
              {{ errors.oldPassword }}
            </p>
          </div>
  
          <!-- 新密碼輸入框 -->
          <div>
            <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">
              新密碼
            </label>
            <input
              v-model="formData.newPassword"
              type="password"
              id="newPassword"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.newPassword }"
              placeholder="請輸入新密碼"
              required
            />
            <p v-if="errors.newPassword" class="mt-1 text-sm text-red-600">
              {{ errors.newPassword }}
            </p>
          </div>
  
          <!-- 確認新密碼輸入框 -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              確認新密碼
            </label>
            <input
              v-model="formData.confirmPassword"
              type="password"
              id="confirmPassword"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.confirmPassword }"
              placeholder="請再次輸入新密碼"
              required
            />
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
              {{ errors.confirmPassword }}
            </p>
          </div>
  
          <!-- 提交按鈕 -->
          <div class="flex justify-end">
            <button
              type="submit"
              class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? '處理中...' : '更新密碼' }}
            </button>
          </div>
        </form>
  
        <!-- 成功訊息和倒數計時 -->
        <div
          v-if="successMessage"
          class="mt-4 p-4 bg-green-100 text-green-700 rounded-md"
        >
          <p>{{ successMessage }}</p>
          <p class="mt-2 font-medium">
            {{ countdown }} 秒後將自動登出並返回登入頁面重新登入
          </p>
        </div>
  
        <!-- 錯誤訊息 -->
        <div
          v-if="apiError"
          class="mt-4 p-4 bg-red-100 text-red-700 rounded-md"
        >
          {{ apiError }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import apiService from '../../api/apiService';
  import Cookies from "js-cookie";
  
  export default {
    name: "Settings",
    setup() {
      const router = useRouter();
      const formData = reactive({
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
  
      const errors = reactive({
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
  
      const isSubmitting = ref(false);
      const successMessage = ref('');
      const apiError = ref('');
      const countdown = ref(0);
      let countdownTimer = null;
  
      const logout = () => {
        Cookies.remove("name");
        Cookies.remove("username");
        Cookies.remove("role");
        Cookies.remove("auth_token");
        router.push('/');
      };
  
      const startCountdown = () => {
        countdown.value = 3;
        countdownTimer = setInterval(() => {
          countdown.value--;
          if (countdown.value <= 0) {
            clearInterval(countdownTimer);
            logout();
          }
        }, 1000);
      };
  
      const validateForm = () => {
        let isValid = true;
        Object.keys(errors).forEach(key => errors[key] = '');
        apiError.value = '';
  
        if (!formData.oldPassword) {
          errors.oldPassword = '請輸入目前密碼';
          isValid = false;
        }
  
        if (!formData.newPassword) {
          errors.newPassword = '請輸入新密碼';
          isValid = false;
        }
  
        if (!formData.confirmPassword) {
          errors.confirmPassword = '請確認新密碼';
          isValid = false;
        } else if (formData.newPassword !== formData.confirmPassword) {
          errors.confirmPassword = '兩次輸入的密碼不相符';
          isValid = false;
        }
  
        return isValid;
      };
  
      const handlePasswordChange = async () => {
        if (!validateForm()) {
          return;
        }
  
        isSubmitting.value = true;
        successMessage.value = '';
        apiError.value = '';
  
        try {
          const username = Cookies.get('username');
          if (!username) {
            throw new Error('找不到使用者名稱');
          }
  
          const response = await apiService.ChangePassword({
            account: username,
            old_password: formData.oldPassword,
            new_password: formData.newPassword
          });
  
          // 清空表單
          formData.oldPassword = '';
          formData.newPassword = '';
          formData.confirmPassword = '';
          successMessage.value = '密碼已成功更改';
          
          // 開始倒數計時
          startCountdown();
  
        } catch (error) {
          if (error.response?.status === 403) {
            apiError.value = '舊密碼不正確';
          } else if (error.message === '找不到使用者名稱') {
            apiError.value = '請先登入後再修改密碼';
          } else {
            apiError.value = '發生錯誤，請稍後再試';
          }
        } finally {
          isSubmitting.value = false;
        }
      };
  
      return {
        formData,
        errors,
        isSubmitting,
        successMessage,
        apiError,
        countdown,
        handlePasswordChange
      };
    }
  };
  </script>