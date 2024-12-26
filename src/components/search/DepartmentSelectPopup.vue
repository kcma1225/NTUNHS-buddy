<template>
  <div
    class="bg-white rounded-lg shadow-lg w-64 h-72 flex flex-col overflow-hidden"
    :style="popupStyle"
    ref="popup"
  >
    <!-- Header Section -->
    <div class="px-3 py-2.5 border-b border-gray-100 flex justify-between items-center">
      <h2 class="text-sm font-semibold text-gray-800">選擇系所分類</h2>
      <button
        type="button"
        class="flex items-center text-xs text-red-600 hover:text-red-700 transition-colors"
        @click="clearAll"
      >
        <i class="bi bi-trash-fill text-xs mr-1"></i>清除
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="px-2 py-1.5 border-b border-gray-100 flex gap-1">
      <button
        type="button"
        class="flex-1 py-1 text-xs font-medium rounded transition-colors"
        :class="!showSelectedOnly 
          ? 'bg-blue-50 text-blue-600' 
          : 'text-gray-500 hover:bg-gray-50'"
        @click="showSelectedOnly = false"
      >
        全部
      </button>
      <button
        type="button"
        class="flex-1 py-1 text-xs font-medium rounded transition-colors"
        :class="showSelectedOnly 
          ? 'bg-blue-50 text-blue-600' 
          : 'text-gray-500 hover:bg-gray-50'"
        @click="showSelectedOnly = true"
      >
        已選
      </button>
    </div>

    <!-- Content Section -->
    <div class="flex-1 overflow-y-auto">
      <div class="p-1">
        <!-- 已選項目 -->
        <template v-if="showSelectedOnly">
          <div 
            v-if="tempSelected.length === 0" 
            class="h-full flex items-center justify-center text-xs text-gray-400 py-4"
          >
            尚未選擇
          </div>
          <div v-else class="space-y-0.5">
            <div
              v-for="dept in tempSelected"
              :key="dept"
              @click="toggleAndApply(dept)"
              class="px-3 py-1.5 text-xs rounded cursor-pointer bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
            >
              {{ dept }}
            </div>
          </div>
        </template>

        <!-- 全部選項 -->
        <template v-else>
          <div v-if="Object.keys(filteredDepartments).length === 0" 
               class="h-full flex items-center justify-center text-xs text-gray-400 py-4">
            無資料
          </div>
          <div v-else class="space-y-2">
            <div 
              v-for="(items, category) in filteredDepartments" 
              :key="category" 
              class="space-y-1"
            >
              <!-- 分類標題 -->
              <div class="px-3 py-1.5 bg-gray-100 text-sm font-semibold text-gray-700 border-y border-gray-200">
                {{ category }}
              </div>
              <!-- 分類項目 -->
              <div class="space-y-0.5">
                <div
                  v-for="dept in items"
                  :key="dept"
                  @click="toggleAndApply(dept)"
                  class="px-3 py-1.5 text-xs rounded cursor-pointer transition-colors"
                  :class="isSelected(dept)
                    ? 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                    : 'text-gray-600 hover:bg-gray-50'"
                >
                  {{ dept }}
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
// Script 部分保持不變
import departmentsData from "/src/assets/data/departments.json";

export default {
  name: "DepartmentSelectPopup",
  props: {
    systemList: { type: Array, default: () => [] },
    selectedItems: { type: Array, default: () => [] },
    style: { type: Object, default: () => ({}) },
    triggerElement: { type: Object, default: null },
  },
  data() {
    return {
      departments: departmentsData,
      filteredDepartments: {},
      tempSelected: [],
      showSelectedOnly: false,
      popupStyle: {},
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
    this.positionPopup();
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
        params.delete("dept");
      }
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
    initFromUrl() {
      const params = new URLSearchParams(window.location.search);
      if (params.get("dept")) {
        this.tempSelected = params.get("dept").split(",");
      } else {
        this.tempSelected = [];
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