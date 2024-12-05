<!-- 
這個檔案拿來做測試的而已。不用刪除或修改 
-->

<template>
    <div id="app">
      <Header @open-news="showNewsPopup" />
      <LoginPopup v-if="isLoginVisible" @close-login="hideLoginPopup" />
      <NewsPopup v-if="isNewsVisible" @close-news="hideNewsPopup" />
    </div>
  </template>
  
  <script>
  import Header from "./components/layout/Header.vue";
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
        isLoginVisible: false,
        isNewsVisible: false,
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
    },
  };
  </script>