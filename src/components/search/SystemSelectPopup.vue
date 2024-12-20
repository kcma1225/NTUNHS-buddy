<template>
    <div
      class="bg-white pt-4 rounded border w-80 h-80 flex flex-col overflow-hidden shadow-lg"
      :style="style"
      ref="popup"
    >
      <div class="flex justify-between items-center mb-2 px-3">
        <h2 class="text-base font-bold">選擇學制名稱</h2>
        <button
          type="button"
          class="flex items-center gap-1 bg-red-100 text-red-700 text-sm px-2 py-1 rounded-full hover:bg-red-200"
          @click="clearAll"
        >
          <i class="bi bi-trash-fill"></i>清除
        </button>
      </div>
  
      <div class="px-2 py-2 flex gap-2 border-b">
        <button
          type="button"
          class="px-3 py-1 rounded hover:bg-gray-200"
          :class="showSelectedOnly ? 'bg-gray-200' : 'bg-white'"
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
  
      <div class="flex-1 overflow-y-auto space-y-1">
        <template v-if="showSelectedOnly">
          <div v-if="tempSelected.length === 0" class="text-gray-500 text-sm px-4 pt-2">尚未選擇</div>
          <div v-else>
            <div
              v-for="sys in tempSelected"
              :key="sys.id"
              class="px-4 py-1 bg-blue-200 text-blue-900 cursor-pointer hover:bg-blue-300"
              @click="toggleAndApply(sys)"
            >
              {{ sys.name }}
            </div>
          </div>
        </template>
        <template v-else>
          <div v-if="systems.length === 0" class="text-gray-500 text-sm">無資料</div>
          <div v-else>
            <div
              v-for="sys in systems"
              :key="sys.id"
              class="px-4 py-1 cursor-pointer"
              :class="isSelected(sys) ? 'bg-blue-200 text-blue-900 hover:bg-blue-300' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
              @click="toggleAndApply(sys)"
            >
              {{ sys.name }}
            </div>
          </div>
        </template>
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
          { id: 1, name: "四技" },
          { id: 2, name: "二技" },
          { id: 3, name: "二技(三年)" },
          { id: 4, name: "學士後系" },
          { id: 5, name: "學士後學位學程" },
          { id: 6, name: "學士後多元專長" },
          { id: 7, name: "碩士班" },
          { id: 8, name: "博士班" },
        ],
        tempSelected: [],
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
        this.updateUrlParams(true); // 清除 dept 參數
        this.$emit("confirm", this.tempSelected);
      },
      clearAll() {
        this.tempSelected = [];
        this.updateUrlParams(true); // 清除 dept 參數
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
        }
        if (clearDept) params.delete("dept"); // 清除 dept 參數
        window.history.replaceState({}, "", `?${params.toString()}`);
      },
      initFromUrl() {
        const params = new URLSearchParams(window.location.search);
        if (params.get("sys")) {
          const sysIds = params.get("sys").split(",").map(Number);
          this.tempSelected = this.systems.filter((sys) => sysIds.includes(sys.id));
        }
      },
    },
  };
  </script>
  