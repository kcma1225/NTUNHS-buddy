<template>
  <!-- Overlay 背景 -->
  <div
    class="fixed inset-0 z-50 bg-black bg-opacity-50 flex justify-center items-center"
    @click.self="cancelChanges"
  >
    <!-- Popup Container -->
    <div class="relative bg-white rounded-lg shadow-lg w-4/5 max-w-5xl h-[80vh] flex flex-col">
      <!-- Header -->
      <div class="border-b px-6 py-3 flex justify-between items-center">
        <span class="font-medium text-lg">篩選條件</span>
        <button
          type="button"
          aria-label="Close"
          @click="cancelChanges"
          class="text-2xl font-bold text-gray-500 hover:text-gray-700 focus:outline-none"
        >
          &times;
        </button>
      </div>

      <!-- Main Content -->
      <div class="flex flex-1 overflow-hidden">
        <!-- 左側內容 -->
        <div class="w-1/2 border-r p-4 overflow-y-auto hide-scrollbar">
          <!-- 學期 -->
          <div class="flex flex-col gap-4 border-b pb-5">
            <div class="font-medium text-base">學期</div>
            <div class="flex gap-2 overflow-x-auto hide-scrollbar">
              <button
                v-for="semester in semesters"
                :key="semester.value"
                @click="toggleSelection('s', semester.value, selectedSemesters)"
                class="shrink-0 select-none rounded-xl border-[1.2px] px-4 py-2.5 text-sm font-medium transition active:scale-95"
                :class="{
                  'bg-green-600 text-white': selectedSemesters.includes(semester.value),
                  'border-gray-300 text-gray-700 hover:bg-gray-200': !selectedSemesters.includes(semester.value),
                }"
              >
                <p class="text-sm">{{ semester.year }}</p>
                <p>{{ semester.term }}</p>
              </button>
            </div>
          </div>

          <!-- 年級 -->
          <div class="flex flex-col gap-4 border-b py-5">
            <div class="font-medium text-base">年級</div>
            <div class="flex gap-2 flex-wrap">
              <button
                v-for="grade in grades"
                :key="grade.value"
                @click="toggleSelection('grade', grade.value, selectedGrades)"
                class="shrink-0 select-none rounded-md border-[1.2px] px-4 py-2 text-sm font-medium transition active:scale-95"
                :class="{
                  'bg-green-600 text-white': selectedGrades.includes(grade.value),
                  'border-gray-300 text-gray-700 hover:bg-gray-200': !selectedGrades.includes(grade.value),
                }"
              >
                {{ grade.label }}
              </button>
            </div>
          </div>

          <!-- 課別 -->
          <div class="flex flex-col gap-4 border-b py-5">
            <div class="font-medium text-base">課別</div>
            <div class="flex gap-2 flex-wrap">
              <button
                v-for="category in courseCategories"
                :key="category.value"
                @click="toggleSelection('category', category.value, selectedCategories)"
                class="shrink-0 select-none rounded-md border-[1.2px] px-4 py-2 text-sm font-medium transition active:scale-95"
                :class="{
                  'bg-green-600 text-white': selectedCategories.includes(category.value),
                  'border-gray-300 text-gray-700 hover:bg-gray-200': !selectedCategories.includes(category.value),
                }"
              >
                {{ category.label }}
              </button>
            </div>
          </div>

          <!-- 課程內容分類 -->
          <div class="flex flex-col gap-4 py-5">
            <div class="font-medium text-base">課程內容分類</div>
            <div class="flex gap-2 flex-wrap">
              <button
                v-for="content in courseContents"
                :key="content.value"
                @click="toggleSelection('content', content.value, selectedContents)"
                class="shrink-0 select-none rounded-md border-[1.2px] px-4 py-2 text-sm font-medium transition active:scale-95"
                :class="{
                  'bg-green-600 text-white': selectedContents.includes(content.value),
                  'border-gray-300 text-gray-700 hover:bg-gray-200': !selectedContents.includes(content.value),
                }"
              >
                {{ content.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- 右側 Grid 表格 -->
        <div class="w-1/2 p-4 overflow-y-auto hide-scrollbar">
          <div class="font-medium text-base mb-3">上課時間</div>
          <table class="w-full border-collapse text-center text-sm">
            <thead>
              <tr>
                <th
                  v-for="day in days"
                  :key="day.value"
                  @click="toggleColumn(day.value)"
                  class="p-2 cursor-pointer"
                  :class="{
                    'text-red-400': day.label === '六' || day.label === '日',
                    'bg-green-600 text-white': isFullColumnSelected(day.value)
                  }"
                >
                  {{ day.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in rows" :key="row">
                <td
                  v-for="day in days"
                  :key="`${day.value}-${row}`"
                  @click="toggleSelection('t', `${day.value}${row}`, selectedTimes)"
                  class="p-2 border cursor-pointer hover:bg-gray-200"
                  :class="{
                    'bg-green-600 text-white': selectedTimes.includes(`${day.value}${row}`)
                  }"
                >
                  {{ row }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>


      <!-- Bottom Buttons -->
      <div class="flex flex-row items-center justify-between gap-2 border-t px-5 py-3">
        <button
          @click="clearSelections"
          class="cursor-pointer rounded-xl p-3 text-sm font-medium text-red-500 transition-transform hover:bg-red-500/5 active:scale-95"
        >
          清除篩選項目
        </button>
        <button
          @click="applyChanges"
          class="cursor-pointer rounded-xl bg-green-600 px-6 py-3 text-sm font-medium text-white transition-transform hover:bg-green-700 active:scale-95"
        >
          搜尋課程
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ButtonSearchPopup",
  data() {
    return {
      semesters: [
        { year: "113", term: "下學期", value: "1132" },
        { year: "113", term: "上學期", value: "1131" },
        { year: "112", term: "下學期", value: "1122" },
        { year: "112", term: "上學期", value: "1121" },
      ],
      grades: [
        { label: "一年級", value: "1" },
        { label: "二年級", value: "2" },
        { label: "三年級", value: "3" },
        { label: "四年級", value: "4" },
      ],
      courseCategories: [
        { label: "通識選修", value: "3" },
        { label: "通識必修", value: "1" },
        { label: "專業選修", value: "4" },
        { label: "專業必修", value: "2" },
      ],    
      courseContents: [
        { label: "跨校", value: "1" },
        { label: "跨域課程", value: "2" },
        { label: "全英語授課", value: "3" },
        { label: "EMI全英語授課", value: "4" },
        { label: "同步遠距教學", value: "5" },
        { label: "非同步遠距教學", value: "6" },
        { label: "混合式遠距教學", value: "7" },
        { label: "遠距教學課程", value: "8" },
        { label: "遠距輔助課程", value: "9" },
        { label: "無", value: "無"}
      ],
      days: [
        { label: "一", value: "1" },
        { label: "二", value: "2" },
        { label: "三", value: "3" },
        { label: "四", value: "4" },
        { label: "五", value: "5" },
        { label: "六", value: "6" },
        { label: "日", value: "7" },
      ],
      rows: Array.from({ length: 14 }, (_, i) => i + 1),
      selectedSemesters: [],
      selectedGrades: [],
      selectedCategories: [],
      selectedContents: [],
      selectedTimes: [],
      selectedColumns: [],
    };
  },
  methods: {
    toggleSelection(param, value, list) {
      const index = list.indexOf(value);
      if (index > -1) list.splice(index, 1);
      else list.push(value);
      this.updateUrlParams(param, list);
    },
    toggleColumn(dayValue) {
      const fullColumn = this.rows.map((row) => `${dayValue}${row}`);
      if (this.isFullColumnSelected(dayValue)) {
        this.selectedTimes = this.selectedTimes.filter((time) => !fullColumn.includes(time));
      } else {
        fullColumn.forEach((cell) => {
          if (!this.selectedTimes.includes(cell)) this.selectedTimes.push(cell);
        });
      }
      this.updateUrlParams("t", this.selectedTimes);
    },
    isFullColumnSelected(dayValue) {
      const fullColumn = this.rows.map((row) => `${dayValue}${row}`);
      return fullColumn.every((cell) => this.selectedTimes.includes(cell));
    },
    updateUrlParams(param, list) {
      const params = new URLSearchParams(window.location.search);
      if (list.length) params.set(param, list.join(","));
      else params.delete(param);
      window.history.replaceState({}, "", `?${params.toString()}`);
    },
    
    clearSelections() {
      this.selectedSemesters = [];
      this.selectedGrades = [];
      this.selectedCategories = [];
      this.selectedContents = [];
      this.selectedTimes = [];
      this.selectedColumns = [];
      this.updateUrlParams("s", []);
      this.updateUrlParams("grade", []);
      this.updateUrlParams("category", []);
      this.updateUrlParams("content", []);
      this.updateUrlParams("t", []);
    },
    applyChanges() {
      this.$emit("close");
    },
    cancelChanges() {
      this.initializeSelections();
      this.$emit("close");
    },
    initializeSelections() {
      const params = new URLSearchParams(window.location.search);
      this.selectedSemesters = params.get("s") ? params.get("s").split(",") : [];
      this.selectedGrades = params.get("grade") ? params.get("grade").split(",") : [];
      this.selectedCategories = params.get("category") ? params.get("category").split(",") : [];
      this.selectedContents = params.get("content") ? params.get("content").split(",") : [];
      this.selectedTimes = params.get("t") ? params.get("t").split(",") : [];
    },
  },
  mounted() {
    this.initializeSelections();
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
.text-red-400 {
  color: #f87171;
}
</style>
