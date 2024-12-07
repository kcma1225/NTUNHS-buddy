<template>
  <div class="news-popup">
    <div class="popup-content">
      <!-- Header -->
      <div class="popup-header" :class="{ 'has-selected-news': !!selectedNews }">
        <!-- 返回列表按鈕 -->
        <button v-if="selectedNews" @click="selectedNews = null" class="back-button">
          <!-- 使用 Bootstrap 的 Chevron Left 圖標 -->
          <i class="bi bi-chevron-left back-icon"></i>
          返回列表
        </button>
        <!-- 標題 -->
        <h2 class="popup-title">{{ selectedNews ? selectedNews.title : "最新消息" }}</h2>
        <!-- 關閉按鈕 -->
        <button @click="$emit('close-news')" class="close-button">✖</button>
      </div>
      <!-- 列表模式 -->
      <div v-if="!selectedNews" class="news-list">
        <ul>
          <li
            v-for="news in newsList"
            :key="news.timestamp"
            @click="viewNews(news)"
            class="news-item"
          >
            <a href="#" class="news-link">
              <span class="news-title">{{ news.title }}</span>
              <span class="news-date">{{ news.date }}</span>
            </a>
          </li>
        </ul>
      </div>
      <!-- 詳細模式 -->
      <div v-else class="news-detail">
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
}

/* Header 樣式 */
.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background-color: #003618;
  color: white;
  height: 50px;
}

.popup-header.has-selected-news {
  justify-content: flex-start;
}

.popup-title {
  font-size: 18px;
  font-weight: bold;
  margin-left: 10px;
  color: white; /* 將標題文字顏色設為白色 */
}

/* 返回列表按鈕樣式 */
.back-button {
  background: none;
  border: none;
  color: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.back-icon {
  margin-right: 5px;
}

/* 關閉按鈕 */
.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: white;
  cursor: pointer;
}

.close-button:hover {
  opacity: 0.8;
}

/* 列表樣式 */
.news-list ul {
  list-style: none;
  padding: 0;
}

.news-item {
  padding-left: 10px; /* 增加左側內邊距 */
  padding-right: 10px;
}

.news-link {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  text-decoration: none;
  border-bottom: 1px solid #ddd;
  color: black;
  cursor: pointer;
}

.news-link:hover {
  background-color: #f0f0f0;
}

.news-title {
  font-weight: bold;
}

.news-date {
  padding-top: 10px;
  padding-left: 10px;
  color: gray;
  font-size: 12px;
}

.news-detail .news-date {
  display: block;
  color: gray;
  font-size: 12px;
  margin-bottom: 10px;
}

.news-content {
  padding-left: 10px;
  margin-top: 10px;
  line-height: 1.6;
}
</style>
