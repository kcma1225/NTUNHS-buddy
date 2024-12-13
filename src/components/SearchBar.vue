<!-- components/SearchBar.vue -->
<template>
    <div class="search-container">
      <input
        type="text"
        class="search-input"
        placeholder="搜尋課程名稱"
        @mouseover="onHover"
        @mouseleave="onLeave"
        :style="inputStyle"
      />
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        inputStyle: {},
      };
    },
    methods: {
      onHover() {
        this.inputStyle = { backgroundColor: "#f5f5f5" }; // 淺灰色
      },
      onLeave() {
        this.inputStyle = { backgroundColor: "#ffffff" }; // 回到白色
      },
    },
  };
  </script>
  
  <style scoped>
  .search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .search-input {
    width: 300px;
    padding: 8px 12px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 20px;
    outline: none;
    transition: background-color 0.3s ease;
  }
  
  .search-input::placeholder {
    color: #bbb;
  }
  </style>
  