<template>
    <div
      class="bg-white pt-4 rounded border w-80 h-80 flex flex-col overflow-hidden shadow-lg"
      :style="style"
      ref="popup"
    >
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
              v-for="dept in tempSelected"
              :key="dept.name"
              class="px-4 py-1 bg-blue-200 text-blue-900 cursor-pointer hover:bg-blue-300"
              @click="toggleAndApply(dept)"
            >
              {{ dept.name }}
            </div>
          </div>
        </template>
        <template v-else>
          <div v-if="departments.length === 0" class="text-gray-500 text-sm">無資料</div>
          <div v-else>
            <div
              v-for="dept in departments"
              :key="dept.name"
              class="px-4 py-1 cursor-pointer"
              :class="isSelected(dept) ? 'bg-blue-200 text-blue-900 hover:bg-blue-300' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
              @click="toggleAndApply(dept)"
            >
              {{ dept.name }}
            </div>
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "DepartmentSelectPopup",
    props: {
      systemList: { type: Array, default: () => [] },
      selectedItems: { type: Array, default: () => [] },
      style: { type: Object, default: () => ({}) },
    },
    data() {
      return {
        departments: [
          { name: "資管系" },
          { name: "健管系" },
          { name: "護理系" },
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
      isSelected(dept) {
        return this.tempSelected.some((d) => d.name === dept.name);
      },
      toggleAndApply(dept) {
        if (this.systemList.length === 0) {
          alert("請先選擇學制");
          return;
        }
        const idx = this.tempSelected.findIndex((d) => d.name === dept.name);
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
          const names = this.tempSelected.map((dept) => dept.name).join(",");
          params.set("dept", names);
        } else {
          params.delete("dept");
        }
        window.history.replaceState({}, "", `?${params.toString()}`);
      },
      initFromUrl() {
        const params = new URLSearchParams(window.location.search);
        if (params.get("dept")) {
          const deptNames = params.get("dept").split(",");
          this.tempSelected = this.departments.filter((dept) =>
            deptNames.includes(dept.name)
          );
        }
      },
    },
  };
  </script>
  
  
  