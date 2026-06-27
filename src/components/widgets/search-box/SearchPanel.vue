<template>
  <Command :should-filter="false">
    <CommandInput placeholder="搜尋你想搜的..." v-model="searchQuery" @keydown.enter="doSearch" />

    <CommandList>
      <CommandEmpty v-if="searchQuery && searchSuggestions.length === 0">
        等等...還在搜尋中！
      </CommandEmpty>

      <CommandGroup heading="搜尋建議">
        <CommandItem
          v-for="suggestion in searchSuggestions"
          :key="suggestion"
          :value="suggestion"
          @select="
            searchQuery = suggestion;
            doSearch();
          "
        >
          {{ suggestion }}
        </CommandItem>
      </CommandGroup>
    </CommandList>
  </Command>
</template>

<script setup lang="ts">
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { ref, onMounted, watch } from "vue";

const searchQuery = ref("");
const searchSuggestions = ref<string[]>([]);
let cooldownTimer: ReturnType<typeof setTimeout> | null = null;

function doSearch() {
  if (!searchQuery.value.trim()) return;
  window.open(`https://www.google.com/search?q=${encodeURIComponent(searchQuery.value)}`, "_blank");
}

function fetchSearchSuggestions(query: string) {
  console.log("Fetching search suggestions for query:", query);
  if (!query.trim()) {
    searchSuggestions.value = [];
    return;
  }

  // 呼叫你自己寫好的 Cloudflare Worker 代理 API
  const API_URL = `https://api.samhacker.xyz/search_suggestions?q=${encodeURIComponent(query)}`;

  fetch(API_URL)
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      // 直接解析後端回傳的 JSON 陣列
      return response.json();
    })
    .then((suggestions: string[]) => {
      console.log("Google Suggestion Data (Parsed):", suggestions);

      // 因為後端回傳的直接就是 ["關鍵字1", "關鍵字2", ...] 陣列
      // 這裡直接切前 7 筆塞給你的響應式變數（如 Vue 的 ref）即可
      searchSuggestions.value = suggestions.slice(0, 7);
    })
    .catch((error) => {
      console.error("Error fetching search suggestions:", error);
      searchSuggestions.value = [];
    });
}

// watch 邏輯保持不變
watch(searchQuery, (newQuery) => {
  if (cooldownTimer) clearTimeout(cooldownTimer);

  console.log("Search query changed:", newQuery);
  if (!newQuery.trim()) {
    // searchSuggestions.value = [];
    return;
  }

  cooldownTimer = setTimeout(() => {
    fetchSearchSuggestions(newQuery);
  }, 500);
});

onMounted(() => {
  searchQuery.value = "";
});
</script>