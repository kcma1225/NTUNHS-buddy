<template>
  <div id="app" class="flex flex-col min-h-screen">
    <Header @open-login="showLoginPopup" @open-news="showNewsPopup" />

    <!-- Main Content Frame -->
    <main class="flex-grow pt-16 bg-gray-100">
      <div class="container mx-auto p-6 bg-white shadow-lg rounded-lg">
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
import Header from "./components/header/Header.vue";
import Footer from "./components/footer/footer.vue";
import LoginPopup from "./components/auth/LoginPopup.vue";
import NewsPopup from "./components/header/NewsPopup.vue";
import ExampleComponent from "./components/ExampleComponent.vue";

export default {
  components: {
    Header,
    Footer,
    LoginPopup,
    NewsPopup,
    ExampleComponent,
  },
  data() {
    return {
      isLoginVisible: false,
      isNewsVisible: false,
      currentComponent: "ExampleComponent",
    };
  },
};
</script>
