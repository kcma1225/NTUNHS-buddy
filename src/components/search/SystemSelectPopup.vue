<template>
  <div
    class="bg-white rounded-lg shadow-lg w-64 h-72 flex flex-col overflow-hidden"
    :style="style"
    ref="popup"
  >
    <!-- Header Section -->
    <div class="px-3 py-2.5 border-b border-gray-100 flex justify-between items-center">
      <h2 class="text-sm font-semibold text-gray-800">選擇學制名稱</h2>
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
        <template v-if="showSelectedOnly">
          <div v-if="tempSelected.length === 0" 
               class="h-full flex items-center justify-center text-xs text-gray-400 py-4">
            尚未選擇
          </div>
          <div v-else class="space-y-0.5">
            <div
              v-for="sys in tempSelected"
              :key="sys.id"
              @click="toggleAndApply(sys)"
              class="px-3 py-1.5 text-xs rounded cursor-pointer bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
            >
              {{ sys.name }}
            </div>
          </div>
        </template>
        <template v-else>
          <div v-if="systems.length === 0" 
               class="h-full flex items-center justify-center text-xs text-gray-400 py-4">
            無資料
          </div>
          <div v-else class="space-y-0.5">
            <div
              v-for="sys in systems"
              :key="sys.id"
              @click="toggleAndApply(sys)"
              class="px-3 py-1.5 text-xs rounded cursor-pointer transition-colors"
              :class="isSelected(sys)
                ? 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                : 'text-gray-600 hover:bg-gray-50'"
            >
              {{ sys.name }}
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SystemSelectPopup",
  props: {
    selectedItems: { type: Array, default: () => [] },
    style: { type: Object, default: () => ({}) },
  },
  data() {
    return {
      systems: [
        { id: "四技", name: "四技" },
        { id: "二技", name: "二技" },
        { id: "二技(三年)", name: "二技(三年)" },
        { id: "學士後系", name: "學士後系" },
        { id: "學士後學位學程", name: "學士後學位學程" },
        { id: "學士後多元專長", name: "學士後多元專長" },
        { id: "碩士班", name: "碩士班" },
        { id: "博士班", name: "博士班" },
      ],
      tempSelected: [],
      showSelectedOnly: false,
      clickHandler: null,
    };
  },
  mounted() {
    this.initFromUrl();
    this.clickHandler = (e) => {
      if (!this.$refs.popup.contains(e.target)) {
        this.$emit("close");
      }
    };
    document.addEventListener("click", this.clickHandler);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.clickHandler);
  },
  methods: {
    isSelected(sys) {
      return this.tempSelected.some((s) => s.id === sys.id);
    },
    toggleAndApply(sys) {
      const idx = this.tempSelected.findIndex((s) => s.id === sys.id);
      if (idx === -1) {
        this.tempSelected.push(sys);
      } else {
        this.tempSelected.splice(idx, 1);
      }
      this.updateUrlParams(true);
      this.$emit("confirm", this.tempSelected);
    },
    clearAll() {
      this.tempSelected = [];
      this.updateUrlParams(true);
      this.$emit("clear-all");
      this.$emit("confirm", this.tempSelected);
    },
    updateUrlParams(clearDept = false) {
      const params = new URLSearchParams(window.location.search);
      if (this.tempSelected.length > 0) {
        const ids = this.tempSelected.map((sys) => sys.id).join(",");
        params.set("sys", ids);
      } else {
        params.delete("sys");
        if (clearDept) params.delete("dept");
      }
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
    initFromUrl() {
      const params = new URLSearchParams(window.location.search);
      if (params.get("sys")) {
        const sysIds = params.get("sys").split(",").map(String);
        this.tempSelected = this.systems.filter((sys) => sysIds.includes(sys.id));
      }
    },
  },
};
</script>