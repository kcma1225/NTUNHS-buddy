<template>
  <div id="app">
    <Header :isLoginVisible="isLoginVisible" @open-login="showLoginPopup" />
    <LoginPopup v-if="isLoginVisible" @close-login="hideLoginPopup" />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import LoginPopup from './components/LoginPopup.vue';

export default {
  components: {
    Header,
    LoginPopup,
  },
  data() {
    return {
      isLoginVisible: false,
    };
  },
  methods: {
    showLoginPopup() {
      this.isLoginVisible = true;
    },
    hideLoginPopup() {
      this.isLoginVisible = false;
    },
  },
};
</script>
