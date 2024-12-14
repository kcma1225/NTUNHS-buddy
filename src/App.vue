<template>
  <div id="app" class="flex flex-col min-h-screen">
    <!-- Header -->
    <Header @open-login="showLoginPopup" @open-news="showNewsPopup" />

    <!-- Main Frame -->
    <main class="flex-grow pt-16 bg-gray-100">
      <div class="container mx-auto p-6 bg-white shadow-lg rounded-lg">
        <!-- 動態內容區域 -->
        <component :is="currentComponent" />
      </div>
    </main>

    <!-- Footer -->
    <Footer />

    <!-- Login 和 News 彈出視窗 -->
    <LoginPopup v-if="isLoginVisible" @close-login="hideLoginPopup" />
    <NewsPopup v-if="isNewsVisible" @close-news="hideNewsPopup" />
  </div>
</template>

<script>
/* View */
import Header from "./components/header/Header.vue";
import Footer from "./components/footer/footer.vue";

/* Popup Frame */
import LoginPopup from "./components/auth/LoginPopup.vue";
import NewsPopup from "./components/header/NewsPopup.vue";

/* Main Frame*/
import ExampleComponent from "./components/ExampleComponent.vue";

export default {
  components: {
    Header,
    Footer,
    LoginPopup,
    NewsPopup,
    ExampleComponent, // 預設載入一個範例組件
  },
  data() {
    return {
      isLoginVisible: false,
      isNewsVisible: false,
      currentComponent: "ExampleComponent", // 預設組件
    };
  },
  methods: {
    showLoginPopup() {
      this.isLoginVisible = true;
    },
    hideLoginPopup() {
      this.isLoginVisible = false;
    },
    showNewsPopup() {
      this.isNewsVisible = true;
    },
    hideNewsPopup() {
      this.isNewsVisible = false;
    },
    loadComponent(componentName) {
      this.currentComponent = componentName; // 切換不同組件
    },
  },
};
</script>

<style>
/* 固定 Header 高度，避免被遮擋 */
.pt-16 {
  padding-top: 4rem; /* Header 高度，16 x 0.25rem = 4rem */
}
</style>
