<template>
    <!-- 大螢幕版 Searching Box -->
    <!-- 新增 @submit.prevent="submitSearch"，將search按鈕改為 type="submit" -->
    <form class="relative z-20 hidden w-full items-center overflow-visible rounded-full border bg-white text-sm shadow transition-colors md:flex"
          @submit.prevent="submitSearch">
      <!-- 關鍵字欄位: type="text" 避免瀏覽器預設的X -->
      <div class="sbi group relative px-4 py-2 flex-1 min-w-[200px]">
        <p class="mb-0.5 truncate text-xs">關鍵字</p>
        <input
          :placeholder="keywordPlaceholder"
          autocomplete="off"
          class="w-full truncate bg-transparent font-medium placeholder:text-black/30 focus:outline-none"
          type="text"
          v-model="localKeyword"
        />
        <input hidden type="submit">
        <!-- 唯一的可用清除關鍵字按鈕 -->
        <button
          v-if="localKeyword"
          type="button"
          class="absolute right-2 top-1/2 -translate-y-1/2 z-10 rounded-full p-1 hover:bg-black/5"
          @click="clearKeyword"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
  
      <!-- 學制名稱欄位 -->
      <div class="sbi group relative w-48 px-4 py-2 hidden md:block" ref="systemField">
        <p class="mb-0.5 truncate text-xs">學制名稱</p>
        <a class="flex w-full truncate font-medium no-underline">
          <span class="truncate">{{ displaySelected(selectedSystems, systemPlaceholder) }}</span>
        </a>
        <button
          v-if="selectedSystems.length > 0"
          type="button"
          class="absolute right-8 top-1/2 -translate-y-1/2 z-10 rounded-full p-1 hover:bg-black/5"
          @click.stop="clearSystems"
        >
          <i class="bi bi-x"></i>
        </button>
        <div class="absolute inset-0 cursor-pointer" @click.stop="openSystemSelect"></div>
      </div>
  
      <!-- 系所分類欄位 -->
      <div class="sbi group relative w-48 px-4 py-2 hidden md:block" ref="deptField">
        <p class="mb-0.5 truncate text-xs">系所分類</p>
        <a class="flex w-full truncate font-medium no-underline">
          <span class="truncate" :class="selectedSystems.length === 0 ? 'text-black/30' : ''">
            <template v-if="selectedSystems.length === 0">
              請先選擇學制名稱
            </template>
            <template v-else>
              {{ displaySelected(selectedDepts, deptPlaceholder) }}
            </template>
          </span>
        </a>
        <button
          v-if="selectedDepts.length > 0"
          type="button"
          class="absolute right-16 top-1/2 -translate-y-1/2 z-10 rounded-full p-1 hover:bg-black/5"
          @click.stop="clearDepts"
        >
          <i class="bi bi-x"></i>
        </button>
        <div class="absolute inset-0 cursor-pointer" @click.stop="openDeptSelect"></div>
      </div>
  
      <!-- 搜尋按鈕: 使用type="submit"及bi bi-search icon -->
      <button
        type="submit"
        title="Search"
        class="absolute right-2 top-1/2 -translate-y-1/2 w-12 h-12 z-0 flex items-center justify-center text-gray-600 hover:text-gray-800 focus:outline-none"
        >
        <i class="bi bi-search text-3xl"></i>
      </button>
    </form>
    
  
    <!-- 小螢幕版 (md以下) -->
    <div class="relative w-full md:hidden">
      <!-- 點擊可打開 MobileSearchPopup -->
      <div @click.stop="openMobileSearch" class="h-16 select-none rounded-full border bg-white px-6 py-3 shadow flex items-center cursor-pointer">
        <i class="bi bi-search text-xl mr-2"></i>
        <span class="text-black/60 truncate">{{ localKeyword || '搜尋課程名稱 / 教師' }}</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CourseSearchBox",
    props: {
      keyword: { type: String, default: "" },
      selectedSystems: { type: Array, default: () => [] },
      selectedDepts: { type: Array, default: () => [] },
    },
    data() {
      return {
        localKeyword: this.keyword,
        keywordPlaceholder: "搜尋課程名稱 / 教師",
        systemPlaceholder: "全部",
        deptPlaceholder: "全部",
      };
    },
    methods: {
      openMobileSearch() {
        this.$emit("open-mobile-search");
      },
      openSystemSelect() {
        this.$emit("open-system-select");
      },
      openDeptSelect() {
        if (this.selectedSystems.length === 0) {
          this.$emit("require-system");
        } else {
          this.$emit("open-dept-select");
        }
      },
      submitSearch() {
        this.updateUrlParams();
        this.$emit("search", {
          keyword: this.localKeyword.trim() || null,
          systems: this.selectedSystems,
          depts: this.selectedDepts,
        });
      },
      clearKeyword() {
        this.localKeyword = "";
        this.updateUrlParams();
      },
      clearSystems() {
        this.$emit("update:selectedSystems", []); // 清除學制
        this.$emit("update:selectedDepts", []);   // 同時清除系所
        this.updateUrlParams(true);              // 更新 URL，清除 sys 和 dept
      },
      clearDepts() {
        this.$emit("update:selectedDepts", []);   // 清除系所
        this.updateUrlParams();
      },
      displaySelected(items, placeholder) {
        if (items.length === 0) {
          return placeholder;
        } else if (items.length === 1) {
          return items[0].name || items[0];
        } else {
          return (items[0].name || items[0]) + " +" + (items.length - 1);
        }
      },
      updateUrlParams(clearDept = false) {
        const params = new URLSearchParams(window.location.search);
  
        // 更新 keyword 參數
        if (this.localKeyword && this.localKeyword.trim()) {
          params.set("keyword", this.localKeyword.trim());
        } else {
          params.delete("keyword");
        }
  
        // 更新 sys 參數 (確保只取出ID並轉成字串)
        if (this.selectedSystems.length > 0) {
          const sysIds = this.selectedSystems.map((sys) => (sys.id ? sys.id : sys)).join(",");
          params.set("sys", sysIds);
        } else {
          params.delete("sys");
          if (clearDept) params.delete("dept"); // 同時清除 dept
        }
  
        // 更新 dept 參數 (確保只取出名稱並轉成字串)
        if (this.selectedDepts.length > 0) {
          const deptNames = this.selectedDepts.map((dept) => (dept.name ? dept.name : dept)).join(",");
          params.set("dept", deptNames);
        } else {
          params.delete("dept");
        }
  
        // 更新網址
        window.history.replaceState({}, "", `?${params.toString()}`);
      },
    },
    mounted() {
      const params = new URLSearchParams(window.location.search);
  
      // 初始化 keyword
      if (params.get("keyword")) {
        this.localKeyword = params.get("keyword");
      }
  
      // 初始化 sys
      if (params.get("sys")) {
        const sysParams = params.get("sys").split(",").map(Number); // 確保轉換為數字陣列
        this.$emit("update:selectedSystems", sysParams);
      }
  
      // 初始化 dept
      if (params.get("dept")) {
        const deptParams = params.get("dept").split(","); // 確保轉換為名稱陣列
        this.$emit("update:selectedDepts", deptParams);
      }
    },
  };
  </script>
  