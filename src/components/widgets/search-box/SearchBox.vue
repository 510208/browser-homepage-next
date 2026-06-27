<template>
  <Button
    class="px-auto h-11 max-h-none w-[300px] border-none bg-white/20 py-2.5 text-center text-base font-light text-white/80 hover:bg-white/30"
    @click="isOpen = true"
  >
    <SearchIcon :size="24" class="size-6 text-brown-500" />
    今天要搜些什麼？
  </Button>

  <!-- 搜尋對話框（由按鈕控制） -->
  <Dialog v-model:open="isOpen">
    <DialogContent as-child class="h-auto w-[400px] gap-0 p-0" aria-describedby="undefined">
      <SearchPanel />
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { SearchIcon } from "@lucide/vue";
import { ref, onMounted, onUnmounted } from "vue";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import SearchPanel from "./SearchPanel.vue";

const isOpen = ref(false);

// 除了w、數字1~9、a鍵以外的任何鍵被按下，就開啟搜尋對話框
function handleKeyDown(event: KeyboardEvent) {
  if (!isOpen.value && event.key !== "w" && event.key !== "a" && !/^[1-9]$/.test(event.key)) {
    isOpen.value = !isOpen.value;
  }
}

onMounted(() => {
  document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeyDown);
});
</script>
