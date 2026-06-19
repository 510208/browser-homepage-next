<template>
  <Input
    placeholder="今天要找些什麼呢"
    v-model="searchQuery"
    @keyup.enter="doSearch"
    class="px-auto h-11 max-h-none w-full max-w-[300px] border-none bg-white/20 py-2.5 text-center text-base! font-light placeholder:text-base placeholder:font-light"
  />
</template>

<script setup lang="ts">
import { Input } from "@/components/ui/input";
import { ref } from "vue";

const searchQuery = ref("");

function doSearch() {
  if (searchQuery.value.trim() !== "") {
    const query = encodeURIComponent(searchQuery.value.trim());
    window.open(`https://www.google.com/search?q=${query}`, "_blank");
  }
}
</script>