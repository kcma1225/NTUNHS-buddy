<template>
  <div id="app">
    <Header @open-login="showLoginPopup" @open-news="showNewsPopup" />
    <LoginPopup v-if="isLoginVisible" @close-login="hideLoginPopup" />
    <NewsPopup v-if="isNewsVisible" @close-news="hideNewsPopup" />
  </div>
</template>

<script>
import Header from "./components/header/Header.vue";
import LoginPopup from "./components/auth/LoginPopup.vue";
import NewsPopup from "./components/header/NewsPopup.vue";

export default {
  components: {
    Header,
    LoginPopup,
    NewsPopup,
  },
  data() {
    return {
      isLoginVisible: false, // 控制 LoginPopup 的顯示
      isNewsVisible: false, // 控制 NewsPopup 的顯示
    };
  },
  methods: {
    showLoginPopup() {
      this.isLoginVisible = true; // 打開 LoginPopup
    },
    hideLoginPopup() {
      this.isLoginVisible = false; // 關閉 LoginPopup
    },
    showNewsPopup() {
      this.isNewsVisible = true; // 打開 NewsPopup
    },
    hideNewsPopup() {
      this.isNewsVisible = false; // 關閉 NewsPopup
    },
  },
};
</script>