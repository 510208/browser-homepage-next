<template>
  <CustomSearchPanel
    v-model="searchQuery"
    :suggestions="searchSuggestions"
    v-model:highlightedIndex="highlightedIndex"
    :loading="isLoading"
    @keydown:down="moveHighlight(1)"
    @keydown:up="moveHighlight(-1)"
    @keydown:enter="selectHighlighted"
    @select="handleSelect"
  />
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import CustomSearchPanel from "@/components/ui/SearchCommandPanel.vue";

// 狀態定義
const searchQuery = ref("");
const searchSuggestions = ref<string[]>([]);
const highlightedIndex = ref(-1); // 目前鍵盤選中的索引
const isLoading = ref(false); // 是否正在發送 API 請求
let cooldownTimer: ReturnType<typeof setTimeout> | null = null;

// 執行 Google 搜尋，在目前分頁開啟新分頁
function doSearch(query: string) {
  const target = query.trim();
  if (!target) return;
  window.open(`https://www.google.com/search?q=${encodeURIComponent(target)}`, "_self");
}

// 當點擊或選取了某個搜尋建議時
function handleSelect(suggestion: string) {
  searchQuery.value = suggestion;
  doSearch(suggestion);
}

// 處理鍵盤上下鍵導覽邏輯
function moveHighlight(direction: number) {
  const total = searchSuggestions.value.length;
  if (total === 0) return;

  // 用取餘數公式來達到循環導覽（到底部再按往下會回到第一個）
  highlightedIndex.value = (highlightedIndex.value + direction + total) % total;
}

// 當在輸入框按下 Enter 鍵時的邏輯
function selectHighlighted() {
  const total = searchSuggestions.value.length;
  // 如果有透過上下鍵高亮某個建議，就搜尋該建議，否則搜尋當前輸入框內容
  if (highlightedIndex.value >= 0 && highlightedIndex.value < total) {
    const selected = searchSuggestions.value[highlightedIndex.value];
    searchQuery.value = selected;
    doSearch(selected);
  } else {
    doSearch(searchQuery.value);
  }
}

// 發送 API 請求
function fetchSearchSuggestions(query: string) {
  console.log("Fetching search suggestions for query:", query);
  if (!query.trim()) {
    searchSuggestions.value = [];
    highlightedIndex.value = -1;
    return;
  }

  isLoading.value = true;
  const API_URL = `https://api.samhacker.xyz/search_suggestions?q=${encodeURIComponent(query)}`;

  fetch(API_URL)
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((suggestions: string[]) => {
      console.log("Google Suggestion Data (Parsed):", suggestions);

      // HTML 實體轉換解碼
      const decoded = suggestions.map((suggestion) => {
        const parser = new DOMParser();
        return parser.parseFromString(suggestion, "text/html").documentElement.textContent || "";
      });

      searchSuggestions.value = decoded.slice(0, 7);
      highlightedIndex.value = -1; // 每次拿到新建議清單，重置高亮
    })
    .catch((error) => {
      console.error("Error fetching search suggestions:", error);
      searchSuggestions.value = [];
      highlightedIndex.value = -1;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

// 監聽輸入框數值變更（Debounce 防抖機制）
watch(searchQuery, (newQuery) => {
  if (cooldownTimer) clearTimeout(cooldownTimer);

  console.log("Search query changed:", newQuery);
  if (!newQuery.trim()) {
    searchSuggestions.value = [];
    highlightedIndex.value = -1;
    return;
  }

  cooldownTimer = setTimeout(() => {
    fetchSearchSuggestions(newQuery);
  }, 500);
});
</script>
