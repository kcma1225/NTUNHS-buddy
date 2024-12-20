<template>
  <div
    class="bg-white pt-4 rounded border w-80 h-80 flex flex-col overflow-hidden shadow-lg"
    :style="popupStyle"
    ref="popup"
  >
    <!-- Header -->
    <div class="flex justify-between items-center mb-2 px-3">
      <h2 class="text-base font-bold">選擇系所分類</h2>
      <button
        type="button"
        class="flex items-center gap-1 bg-red-100 text-red-700 text-sm px-2 py-1 rounded-full hover:bg-red-200"
        @click="clearAll"
      >
        <i class="bi bi-trash-fill"></i>清除
      </button>
    </div>

    <!-- Tabs -->
    <div class="px-2 py-2 flex gap-2 border-b">
      <button
        type="button"
        class="px-3 py-1 rounded hover:bg-gray-200"
        :class="!showSelectedOnly ? 'bg-gray-200' : 'bg-white'"
        @click="showSelectedOnly = false"
      >
        全部
      </button>
      <button
        type="button"
        class="px-3 py-1 rounded hover:bg-gray-200"
        :class="showSelectedOnly ? 'bg-gray-200' : 'bg-white'"
        @click="showSelectedOnly = true"
      >
        已選
      </button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto space-y-1">
      <!-- 已選項目 -->
      <template v-if="showSelectedOnly">
        <div v-if="tempSelected.length === 0" class="text-gray-500 text-sm px-4 pt-2">
          尚未選擇
        </div>
        <div v-else>
          <div
            v-for="dept in tempSelected"
            :key="dept"
            class="px-4 py-1 bg-blue-200 text-blue-900 cursor-pointer hover:bg-blue-300"
            @click="toggleAndApply(dept)"
          >
            {{ dept }}
          </div>
        </div>
      </template>

      <!-- 全部選項 -->
      <template v-else>
        <div v-for="(items, category) in filteredDepartments" :key="category" class="px-2">
          <!-- 大標題 -->
          <h3 class="font-bold text-sm text-gray-700">{{ category }}</h3>
          <!-- 子選項 -->
          <div
            v-for="dept in items"
            :key="dept"
            class="px-4 py-1 cursor-pointer"
            :class="isSelected(dept) ? 'bg-blue-200 text-blue-900 hover:bg-blue-300' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="toggleAndApply(dept)"
          >
            {{ dept }}
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import departmentsData from "/src/assets/data/departments.json";

export default {
  name: "DepartmentSelectPopup",
  props: {
    systemList: { type: Array, default: () => [] }, // 學制列表
    selectedItems: { type: Array, default: () => [] }, // 已選項目
    style: { type: Object, default: () => ({}) },
    triggerElement: { type: Object, default: null }, // 傳入觸發按鈕的 DOM 元素
  },
  data() {
    return {
      departments: departmentsData,
      filteredDepartments: {},
      tempSelected: [],
      showSelectedOnly: false,
      popupStyle: {}, // 彈出視窗的動態位置
    };
  },
  watch: {
    systemList: {
      handler(newVal) {
        this.filterDepartments(newVal);
      },
      immediate: true,
    },
  },
  mounted() {
    this.initFromUrl();
    this.filterDepartments(this.systemList);
    this.positionPopup(); // 設定彈窗位置
    document.addEventListener("click", this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleOutsideClick);
  },
  methods: {
    positionPopup() {
      if (this.triggerElement) {
        const rect = this.triggerElement.getBoundingClientRect();
        this.popupStyle = {
          position: "absolute",
          top: `${rect.bottom + window.scrollY}px`,
          left: `${rect.left + window.scrollX}px`,
          zIndex: 9999,
        };
      }
    },
    filterDepartments(systemList) {
      this.filteredDepartments = {};
      systemList.forEach((sys) => {
        if (this.departments[sys]) {
          this.filteredDepartments[sys] = this.departments[sys];
        }
      });
    },
    isSelected(dept) {
      return this.tempSelected.includes(dept);
    },
    toggleAndApply(dept) {
      const idx = this.tempSelected.indexOf(dept);
      if (idx === -1) {
        this.tempSelected.push(dept);
      } else {
        this.tempSelected.splice(idx, 1);
      }
      this.updateUrlParams();
      this.$emit("confirm", this.tempSelected);
    },
    clearAll() {
      this.tempSelected = [];
      this.updateUrlParams();
      this.$emit("clear-all");
      this.$emit("confirm", this.tempSelected);
    },
    updateUrlParams() {
      const params = new URLSearchParams(window.location.search);
      if (this.tempSelected.length > 0) {
        params.set("dept", this.tempSelected.join(","));
      } else {
        params.delete("dept"); // 清除參數
      }
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
    initFromUrl() {
      const params = new URLSearchParams(window.location.search);
      if (params.get("dept")) {
        this.tempSelected = params.get("dept").split(",");
      } else {
        this.tempSelected = []; // 確保無參數時不會顯示 undefined
      }
    },
    handleOutsideClick(event) {
      if (this.$refs.popup && !this.$refs.popup.contains(event.target)) {
        this.$emit("close");
      }
    },
  },
};
</script>
