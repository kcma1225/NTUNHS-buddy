<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" @click.self="$emit('close-news')">
    <div class="bg-white w-4/5 max-w-4xl h-[600px] rounded-lg overflow-hidden shadow-lg flex flex-col">
      <!-- Header -->
      <div
        :class="[
          'flex items-center justify-between px-4 py-2 bg-green-900 text-white',
          { 'justify-start': !!selectedNews }
        ]"
      >
        <!-- 返回列表按鈕 -->
        <button
          v-if="selectedNews"
          @click="selectedNews = null"
          class="text-white text-sm flex items-center cursor-pointer"
        >
          <i class="bi bi-arrow-return-left mr-1"></i>
          返回列表
        </button>
        <h2 class="text-lg font-bold ml-2">{{ selectedNews ? selectedNews.title : "最新消息" }}</h2>
        <button
          type="button"
          aria-label="Close"
          @click="$emit('close-news')"
          class="text-white text-2xl font-bold cursor-pointer"
        >
          &times;
        </button>
      </div>
      <!-- 列表模式 -->
      <div v-if="!selectedNews" class="flex-grow p-4 overflow-auto">
        <ul class="list-none p-0">
          <li
            v-for="(news, index) in paginatedNews"
            :key="news.timestamp"
            @click="viewNews(news)"
            class="cursor-pointer hover:bg-gray-200 px-4 py-2 border-b border-gray-300 flex items-center"
          >
            <!-- 編號 -->
            <span class="mr-4 font-bold">{{ (currentPage - 1) * itemsPerPage + index + 1 }}.</span>
            <!-- 文章內容 -->
            <a href="#" class="flex justify-between flex-grow items-center text-black no-underline">
              <span class="font-bold">{{ news.title }}</span>
              <span class="text-gray-500 text-xs">{{ news.date }}</span>
            </a>
          </li>
        </ul>
      </div>
      <!-- 詳細模式 -->
      <div v-else class="p-4 flex-grow overflow-auto">
        <span class="block text-gray-500 text-xs mb-2">{{ selectedNews.date }}</span>
        <p class="px-2 mt-2 leading-relaxed" v-html="selectedNews.content"></p>
      </div>
      <!-- 分頁控制 -->
      <div class="p-4 flex justify-center">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
          class="mx-1 px-3 py-1 border rounded"
          :class="{'bg-green-600 text-white': currentPage === page, 'bg-gray-100': currentPage !== page}"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newsList: [
        { timestamp: 1701686400000, date: "2024/08/05", title: "1131校際課程交換日期", content: "詳細資訊請參考以下連結：<a href='http://example.com/calendar'>點擊此處</a>" },
        { timestamp: 1701648000000, date: "2024/08/02", title: "113學年第一學期課程公告日期", content: "第一學期課程公告將於此日公布，敬請關注教務處網站。" },
        { timestamp: 1701648000001, date: "2024/08/02", title: "113學年度行事曆", content: "行事曆詳細資訊，請參閱校方公告：<a href='http://example.com/calendar'>點擊此處</a>" },
        ...Array.from({ length: 10 }, (_, i) => ({
          timestamp: Date.now() + i,
          date: `2024/08/${i + 3}`,
          title: `測試消息標題 ${i + 1}`,
          content: `這是測試消息內容 ${i + 1}，用於模擬更多新聞資料。`
        }))
      ],
      selectedNews: null,
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.sortedNewsList.length / this.itemsPerPage);
    },
    paginatedNews() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedNewsList.slice(start, end);
    },
    sortedNewsList() {
      return this.newsList.sort((a, b) => b.timestamp - a.timestamp);
    }
  },
  methods: {
    viewNews(news) {
      this.selectedNews = news;
    },
  },
};
</script>
