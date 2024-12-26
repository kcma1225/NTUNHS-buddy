<template>
  <div id="app" class="flex flex-col min-h-screen">
    <!-- 路由顯示區域 -->
    <router-view />
  </div>
</template>

<script>
import Cookies from "js-cookie";

export default {
  name: "App",
  created() {
    this.$router.beforeEach((to, from, next) => {
      const role = Cookies.get("role");

      // 檢測是否有權訪問 /admin
      if (to.path.startsWith("/admin") && role !== "admin") {
        next("/"); // 跳轉到根目錄
      }
      // 檢測是否有權訪問 /student
      else if (to.path.startsWith("/student") && role !== "student") {
        next("/"); // 跳轉到根目錄
      } else {
        next();
      }
    });
  },
};
</script>

<style scoped>
/* 全局樣式，根據需要添加 */
</style>
