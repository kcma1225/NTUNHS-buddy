<template>
  <!-- 大螢幕版 Searching Box -->
  <form
    class="relative z-20 hidden w-full items-center overflow-visible rounded-full border text-sm shadow transition-colors md:flex"
    @submit.prevent="submitSearch"
  >
    <!-- 關鍵字欄位 -->
    <div class="sbi group relative px-4 py-2 flex-1 min-w-[200px]">
      <p class="mb-0.5 truncate text-xs">關鍵字</p>
      <input
        :placeholder="keywordPlaceholder"
        autocomplete="off"
        class="w-full truncate bg-transparent font-medium placeholder:text-black/30 focus:outline-none"
        type="text"
        v-model="localKeyword"
      />
      <input hidden type="submit" />
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
      <div class="absolute inset-0 cursor-pointer" @click.stop="openSystemSelect"></div>
    </div>

    <!-- 系所分類欄位 -->
    <div class="sbi group relative w-80 px-4 py-2 hidden md:block" ref="deptField">
      <p class="mb-0.5 truncate text-xs">系所分類</p>
      <a class="flex w-full truncate font-medium no-underline">
        <span
          class="truncate"
          :class="selectedSystems.length === 0 ? 'text-black/30' : ''"
        >
          <template v-if="selectedSystems.length === 0">請先選擇學制名稱</template>
          <template v-else>
            {{ displaySelected(selectedDepts, deptPlaceholder) }}
          </template>
        </span>
      </a>
      <div class="absolute inset-0 cursor-pointer" @click.stop="openDeptSelect"></div>
    </div>

    <!-- 搜尋按鈕 -->
    <button
      type="submit"
      title="Search"
      class="absolute right-2 top-1/2 -translate-y-1/2 w-12 h-12 z-0 flex items-center justify-center text-gray-600 hover:text-gray-800 focus:outline-none"
    >
      <i class="bi bi-search text-3xl"></i>
    </button>
  </form>

    <!-- 彈出式視窗 -->
  <DepartmentSelectPopup
    v-if="isDeptPopupVisible"
    :systemList="selectedSystems.map((sys) => sys.id)"
    :selectedItems="selectedDepts"
    :triggerElement="$refs.deptField"
    @confirm="updateSelectedDepts"
    @close="isDeptPopupVisible = false"
  />

  <!-- 小螢幕版 (md以下) -->
  <div class="relative w-full md:hidden">
    <div
      @click.stop="openMobileSearch"
      class="h-16 select-none rounded-full border bg-white px-6 py-3 shadow flex items-center cursor-pointer"
    >
      <i class="bi bi-search text-xl mr-2"></i>
      <span class="text-black/60 truncate">{{ localKeyword || "搜尋課程名程 / 教師" }}</span>
    </div>
  </div>

  <!-- 新增的按鈕列 -->
  <div
    class="flex gap-3 mt-4 px-4 md:justify-center hide-scrollbar flex gap-2 overflow-x-auto hide-scrollbar"
  >
    <button
      class="shrink-0 select-none rounded-lg border-[1.2px] border-gray-300 bg-white px-2.5 py-1.5 text-sm transition duration-200 first:ml-auto last:mr-auto hover:bg-gray-300 hover:text-gray-900 focus-visible:bg-gray-300 focus-visible:outline-none active:bg-gray-300 md:font-medium text-gray-700 text-center"
      @click="openPopup('進階搜尋')"
    >
      進階搜尋
    </button>
  </div>

  <!-- 彈出式視窗 -->
  <ButtonSearchPopup v-if="isPopupVisible" @close="isPopupVisible = false" />


</template>



<script>
import ButtonSearchPopup from "./ButtonSearchPopup.vue";
import DepartmentSelectPopup from "./DepartmentSelectPopup.vue";

export default {
  name: "CourseSearchBox",
  components: {
    ButtonSearchPopup,
    DepartmentSelectPopup
  },
  props: {
    keyword: { type: String, default: "" },
    selectedSystems: { type: Array, default: () => [] },
    selectedDepts: { type: Array, default: () => [] },
  },
  data() {
    return {
      localKeyword: this.keyword,
      keywordPlaceholder: "搜尋課程名程 / 教師",
      systemPlaceholder: "全部",
      deptPlaceholder: "全部",
      buttonOptions: ["進階搜尋"], // 修改為只保留「進階搜尋」
      isPopupVisible: false,
      isDeptPopupVisible: false,
    };
  },
  methods: {
    openDeptSelect() {
      if (this.selectedSystems.length === 0) {
        this.$emit("require-system");
      } else {
        this.isDeptPopupVisible = true;
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
    updateSelectedDepts(newDepts) {
      this.$emit("update:selectedDepts", newDepts);
      this.updateUrlParams();
    },
    
    openMobileSearch() {
      this.$emit("open-mobile-search");
    },
    openSystemSelect() {
      this.$emit("open-system-select");
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
      if (this.localKeyword && this.localKeyword.trim()) {
        params.set("keyword", this.localKeyword.trim());
      } else {
        params.delete("keyword");
      }
      if (this.selectedSystems.length > 0) {
        const sysIds = this.selectedSystems.map((sys) => (sys.id ? sys.id : sys)).join(",");
        params.set("sys", sysIds);
      } else {
        params.delete("sys");
        if (clearDept) params.delete("dept");
      }
      if (this.selectedDepts.length > 0) {
        const deptNames = this.selectedDepts.map((dept) => (dept.name ? dept.name : dept)).join(",");
        params.set("dept", deptNames);
      } else {
        params.delete("dept");
      }
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
  },
  mounted() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("keyword")) this.localKeyword = params.get("keyword");
  },
};
</script>

<style scoped>
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
