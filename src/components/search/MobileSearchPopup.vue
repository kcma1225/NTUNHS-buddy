<template>
    <div class="fixed inset-0 bg-white z-50 flex flex-col">
      <!-- Header: 返回按鈕和搜尋框 -->
      <div class="shadow-md p-4 flex items-center space-x-2">
        <button @click="closePopup" class="text-2xl">
          <i class="bi bi-arrow-left"></i>
        </button>
        <div class="relative flex-1">
          <input
            v-model="localKeyword"
            type="text"
            placeholder="搜尋課程名稱 / 教師"
            class="w-full border-none p-2 outline-none"
          />
          <!-- 清除搜尋欄的X -->
          <button v-if="localKeyword" @click="clearKeyword" class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-600">
            <i class="bi bi-x-circle-fill text-xl"></i>
          </button>
        </div>
      </div>
    
      <!-- 學制選擇 -->
      <div class="mt-4 px-4">
        <div class="flex justify-between items-center">
          <button
            class="flex items-center w-full py-2 text-lg font-medium"
            @click="toggleSystem"
          >
            學制選擇
            <span v-if="selectedSystems.length > 0" class="ml-2 text-lime-800">
              {{ displaySelectedSystems }}
            </span>
            <i :class="systemOpen ? 'bi bi-chevron-up' : 'bi bi-chevron-down'" class="ml-2"></i>
          </button>
          <button
            v-if="selectedSystems.length > 0"
            class="text-gray-500 hover:bg-gray-300 rounded px-2 py-1 hover:text-red-600 text-sm transition"
            @click="clearSystems"
          >
            清除
          </button>
        </div>
        <div v-show="systemOpen" class="mt-2 h-48 overflow-y-auto border rounded shadow">
          <div
            v-for="system in systems"
            :key="system.id"
            class="cursor-pointer p-2 hover:bg-gray-200 flex items-center"
            :class="{'bg-lime-200 border-2 border-lime-800 rounded': selectedSystems.includes(system.id)}"
            @click="toggleSelectSystem(system.id)"
          >
            <span>{{ system.name }}</span>
          </div>
        </div>
      </div>
    
      <!-- 系所選擇 -->
      <div class="mt-4 px-4">
        <div class="flex justify-between items-center">
          <button
            class="flex items-center w-full py-2 text-lg font-medium"
            @click="toggleDepartment"
            :disabled="selectedSystems.length === 0"
          >
            系所選擇
            <span v-if="selectedDepts.length > 0" class="ml-2 text-lime-800">
              {{ displaySelectedDepts }}
            </span>
            <i :class="deptOpen ? 'bi bi-chevron-up' : 'bi bi-chevron-down'" class="ml-2"></i>
          </button>
          <button
            v-if="selectedDepts.length > 0"
            class="text-gray-500 hover:bg-gray-300 rounded px-2 py-1 hover:text-red-600 text-sm transition"
            @click="clearDepts"
          >
            清除
          </button>
        </div>
        <div v-show="deptOpen" class="mt-2 h-48 overflow-y-auto border rounded shadow">
          <div
            v-for="dept in departments"
            :key="dept"
            class="cursor-pointer p-2 hover:bg-gray-200 flex items-center"
            :class="{'bg-lime-200 border-2 border-lime-800 rounded': selectedDepts.includes(dept)}"
            @click="toggleSelectDepartment(dept)"
          >
            <span>{{ dept }}</span>
          </div>
        </div>
      </div>
    
      <!-- Footer -->
      <div class="border-t mt-auto py-4 flex justify-end items-center">
        <button
          class="bg-lime-800 text-white px-6 py-2 rounded hover:bg-blue-500 shadow mr-4"
          @click="confirmSearch"
        >
          搜尋課程
        </button>
      </div>
    </div>
</template>
    
<script>
export default {
  props: {
    keyword: { type: String, default: "" },
  },
  data() {
    return {
      localKeyword: this.keyword,
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
      departments: [
        "資管系",
        "電機系",
        "機械系",
        "土木系",
        "化工系",
        "醫工系",
        "材料系"
      ],
      selectedSystems: [],
      selectedDepts: [],
      systemOpen: false,
      deptOpen: false,
    };
  },
  computed: {
    displaySelectedSystems() {
      if (this.selectedSystems.length === 0) return "";
      const names = this.selectedSystems.map(id => this.systems.find(s => s.id === id).name);
      return names.length > 1 ? `${names[0]} +${names.length - 1}` : names[0];
    },
    displaySelectedDepts() {
      if (this.selectedDepts.length === 0) return "";
      return this.selectedDepts.length > 1 ? `${this.selectedDepts[0]} +${this.selectedDepts.length - 1}` : this.selectedDepts[0];
    },
  },
  methods: {
    closePopup() {
      this.$emit("update:keyword", this.localKeyword);
      this.$emit("close");
    },
    toggleSystem() {
      this.systemOpen = !this.systemOpen;
    },
    toggleDepartment() {
      if (this.selectedSystems.length > 0) {
        this.deptOpen = !this.deptOpen;
      }
    },
    toggleSelectSystem(systemId) {
      if (this.selectedSystems.includes(systemId)) {
        this.selectedSystems = this.selectedSystems.filter(id => id !== systemId);
      } else {
        this.selectedSystems.push(systemId);
      }
      this.clearDepts(); // 清空系所
      this.updateUrlParams();
    },
    toggleSelectDepartment(dept) {
      if (this.selectedDepts.includes(dept)) {
        this.selectedDepts = this.selectedDepts.filter(d => d !== dept);
      } else {
        this.selectedDepts.push(dept);
      }
      this.updateUrlParams();
    },
    clearKeyword() {
      this.localKeyword = "";
      this.updateUrlParams();
    },
    clearSystems() {
      this.selectedSystems = [];
      this.clearDepts(); // 清空系所
      this.updateUrlParams();
    },
    clearDepts() {
      this.selectedDepts = [];
      this.updateUrlParams();
    },
    confirmSearch() {
      console.log("搜尋資料: ", {
        keyword: this.localKeyword,
        systems: this.selectedSystems,
        departments: this.selectedDepts,
      });
      this.updateUrlParams();
      this.$emit("update:keyword", this.localKeyword);
      this.$emit("update:selectedSystems", this.selectedSystems);
      this.$emit("update:selectedDepts", this.selectedDepts);
      this.refreshPage();
    },
    updateUrlParams() {
      const params = new URLSearchParams(window.location.search);
      if (this.localKeyword) params.set("keyword", this.localKeyword);
      else params.delete("keyword");
      
      if (this.selectedSystems.length > 0) params.set("sys", this.selectedSystems.join(","));
      else params.delete("sys");

      if (this.selectedDepts.length > 0) params.set("dept", this.selectedDepts.join(","));
      else params.delete("dept");
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
    refreshPage() {
      window.location.reload();
    },
  },
  mounted() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("keyword")) this.localKeyword = params.get("keyword");
    if (params.get("sys")) this.selectedSystems = params.get("sys").split(",").map(Number);
    if (params.get("dept")) this.selectedDepts = params.get("dept").split(",");
  },
};
</script>

<style scoped>
/* Tailwind CSS is used in template */
</style>
