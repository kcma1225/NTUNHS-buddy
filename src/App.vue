<template>
  <div id="app" class="flex flex-col min-h-screen">
    <Header @open-login="showLoginPopup" @open-news="showNewsPopup" />
    
    <main class="flex-grow pt-16 bg-gray-100">
      <div class="p-4 w-full">
        <div class="mb-3.5 mt-2 flex items-center justify-center gap-2 w-full">
          <div class="max-w-2xl w-full">
            <!-- Searching Box -->
            <CourseSearchBox
              @open-system-select="openSystemPopup"
              @open-dept-select="openDeptPopup"
              @require-system="handleRequireSystem"
              @search="handleSearch"
              :selectedSystems="selectedSystems"
              :selectedDepts="selectedDepts"
              :keyword="keyword"
              @update:keyword="keyword = $event"
              @update:selectedSystems="selectedSystems = $event"
              @update:selectedDepts="selectedDepts = $event"
              @open-mobile-search="showPopup = true"
              @open-popup="showButtonSearchPopup"
              ref="courseSearchBox"
            />
            <!-- 手機版 Popup -->
            <MobileSearchPopup
              v-if="showPopup"
              :keyword="keyword"
              @update:keyword="updateKeyword"
              @close="showPopup = false"
            />
          </div>
        </div>
      </div>
    </main>

    <Footer />

    <!-- Login 和 News Popup -->
    <LoginPopup v-if="isLoginVisible" @close-login="hideLoginPopup" />
    <NewsPopup v-if="isNewsVisible" @close-news="hideNewsPopup" />

    <!-- 學制選擇 Popup -->
    <SystemSelectPopup
      v-if="showSystemPopup"
      class="absolute z-50"
      :selectedItems="selectedSystems"
      :style="systemPopupStyle"
      @confirm="handleSystemSelected"
      @clear-all="handleSystemClearAll"
      @close="showSystemPopup = false"
    />

    <!-- 系所選擇 Popup -->
    <DepartmentSelectPopup
      v-if="showDeptPopup"
      class="absolute z-50"
      :systemList="selectedSystems"
      :selectedItems="selectedDepts"
      :style="deptPopupStyle"
      @confirm="handleDeptSelected"
      @clear-all="handleDeptClearAll"
      @close="showDeptPopup = false"
    />

    <!-- 新增 ButtonSearchPopup -->
    <ButtonSearchPopup v-if="isButtonSearchPopupVisible" @close="isButtonSearchPopupVisible = false" />
  </div>
</template>

<script>
import Header from "./components/header/Header.vue";
import Footer from "./components/footer/Footer.vue";
import LoginPopup from "./components/auth/LoginPopup.vue";
import NewsPopup from "./components/header/NewsPopup.vue";
import CourseSearchBox from "./components/search/CourseSearchBox.vue";
import SystemSelectPopup from "./components/search/SystemSelectPopup.vue";
import DepartmentSelectPopup from "./components/search/DepartmentSelectPopup.vue";
import MobileSearchPopup from "./components/search/MobileSearchPopup.vue";
import ButtonSearchPopup from "./components/search/ButtonSearchPopup.vue"; // 引入 ButtonSearchPopup

export default {
  components: {
    Header,
    Footer,
    LoginPopup,
    NewsPopup,
    CourseSearchBox,
    SystemSelectPopup,
    DepartmentSelectPopup,
    MobileSearchPopup,
    ButtonSearchPopup, // 註冊 ButtonSearchPopup
  },
  data() {
    return {
      isLoginVisible: false,
      isNewsVisible: false,
      showSystemPopup: false,
      showDeptPopup: false,
      showPopup: false, // 控制 MobileSearchPopup
      isButtonSearchPopupVisible: false, // 新增的 Popup 控制變數
      keyword: "",
      selectedSystems: [],
      selectedDepts: [],
      systemPopupStyle: {
        position: 'absolute',
        top: '0px',
        left: '0px'
      },
      deptPopupStyle: {
        position: 'absolute',
        top: '0px',
        left: '0px'
      }
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
    handleRequireSystem() {
      this.openSystemPopup();
    },
    handleSystemSelected(selectedArray) {
      this.selectedSystems = selectedArray;
    },
    handleDeptSelected(selectedArray) {
      this.selectedDepts = selectedArray;
    },
    handleSearch({ keyword, systems, depts }) {
      console.log("搜尋條件", { keyword, systems, depts });
    },
    openSystemPopup() {
      this.showDeptPopup = false;
      this.$nextTick(() => {
        const el = this.$refs.courseSearchBox.$refs.systemField;
        if (el) {
          const rect = el.getBoundingClientRect();
          this.systemPopupStyle = {
            position: 'absolute',
            top: rect.bottom + window.scrollY + 'px',
            left: rect.left + 'px',
            zIndex: 9999
          };
        }
      });
      this.showSystemPopup = true;
    },
    openDeptPopup() {
      this.showSystemPopup = false;
      if (this.selectedSystems.length === 0) {
        this.showSystemPopup = true;
        return;
      }
      this.$nextTick(() => {
        const el = this.$refs.courseSearchBox.$refs.deptField;
        if (el) {
          const rect = el.getBoundingClientRect();
          this.deptPopupStyle = {
            position: 'absolute',
            top: rect.bottom + window.scrollY + 'px',
            left: rect.left + 'px',
            zIndex: 9999
          };
        }
      });
      this.showDeptPopup = true;
    },
    showButtonSearchPopup() {
      this.isButtonSearchPopupVisible = true; // 開啟 ButtonSearchPopup
    },
    updateKeyword(newKeyword) {
      this.keyword = newKeyword;
    },
    handleSystemClearAll() {
      this.selectedSystems = [];
      this.selectedDepts = [];
    },
    handleDeptClearAll() {
      this.selectedDepts = [];
    }
  },
};
</script>
