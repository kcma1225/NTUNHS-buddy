<template>
    <div class="news-popup">
      <div class="popup-content">
        <div class="popup-header">
          <button @click="$emit('close-news')" class="close-button">✖</button>
          <h2 class="popup-title">最新消息</h2>
        </div>
        <!-- 列表模式 -->
        <div v-if="!selectedNews" class="news-list">
          <ul>
            <li
              v-for="news in newsList"
              :key="news.timestamp"
              @click="viewNews(news)"
            >
              <a href="#" class="news-item">
                <span class="news-title">{{ news.title }}</span>
                <span class="news-date">{{ news.date }}</span>
              </a>
            </li>
          </ul>
        </div>
        <!-- 詳細模式 -->
        <div v-else class="news-detail">
          <button @click="selectedNews = null" class="back-button">返回列表</button>
          <h2 class="news-title">{{ selectedNews.title }}</h2>
          <span class="news-date">{{ selectedNews.date }}</span>
          <p class="news-content" v-html="selectedNews.content"></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newsList: [
          {
            timestamp: 1701686400000,
            date: "2024/08/05",
            title: "1131校際課程交換日期",
            content:
              "詳細資訊請參考以下連結：<a href='http://curri.aca.ntu.edu.tw/aca_doc/Alliance/allp.pdf'>點擊此處</a>",
          },
          {
            timestamp: 1701648000000,
            date: "2024/08/02",
            title: "113學年第一學期課程公告日期",
            content:
              "第一學期課程公告將於此日公布，敬請關注教務處網站。",
          },
          {
            timestamp: 1701648000001,
            date: "2024/08/02",
            title: "113學年度行事曆",
            content:
              "行事曆詳細資訊，請參閱校方公告：<a href='http://example.com/calendar'>點擊此處</a>",
          },
        ],
        selectedNews: null,
      };
    },
    methods: {
      viewNews(news) {
        this.selectedNews = news;
      },
    },
  };
  </script>
  
  <style scoped>
  .news-popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  .popup-content {
    background-color: white;
    width: 90%;
    max-width: 600px;
    border-radius: 8px;
    overflow: hidden;
    padding: 20px;
  }
  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #ddd;
  }
  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  .popup-title {
    font-size: 20px;
    font-weight: bold;
  }
  .news-list ul {
    list-style: none;
    padding: 0;
  }
  .news-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    text-decoration: none;
    border-bottom: 1px solid #ddd;
    color: black;
    cursor: pointer;
  }
  .news-item:hover {
    background-color: #f0f0f0;
  }
  .news-title {
    font-weight: bold;
  }
  .news-date {
    color: gray;
    font-size: 12px;
  }
  .news-detail .back-button {
    background: none;
    border: none;
    color: blue;
    cursor: pointer;
    margin-bottom: 20px;
  }
  .news-content {
    margin-top: 10px;
  }
  </style>
  