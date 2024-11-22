<template>
  <div id="app">
    <HeaderBar />
    <main>
      <h1>歡迎來到北護課程查詢系統！</h1>
      <p>請使用上方導覽列進行操作。</p>
    </main>
  </div>
</template>

<script>
import HeaderBar from './components/HeaderBar.vue';
import './assets/css/app.css';

export default {
  name: 'App',
  components: {
    HeaderBar,
  },
  mounted() {
    window.scrollTo(0, 0);
  },
};
</script>