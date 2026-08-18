<script setup lang="ts">
import { Copy, Search, X } from "@lucide/vue";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";
import { toast } from "vue-sonner";

const props = defineProps<{
  languageLabel?: string;
}>();

const emit = defineEmits<{
  (e: "clear"): void;
  (e: "search"): void;
  (e: "copy", text: string): void;
}>();

// 改用 defineModel 接軌 TranslateDialog 的 v-model:source-text
const sourceText = defineModel<string>("sourceText", { default: "" });

const handleClear = () => {
  sourceText.value = "";
  emit("clear");
};

const handleSearch = () => {
  // 如果 sourceText 為空，則不觸發搜尋事件
  if (!sourceText.value.trim()) {
    return;
  }

  // 導向Google搜尋頁面，並將 sourceText 作為查詢參數傳遞
  const googleSearchUrl = `https://www.google.com/search?q=${encodeURIComponent(sourceText.value)}`;
  window.open(googleSearchUrl, "_blank");

  emit("search");
};

const handleCopy = () => {
  navigator.clipboard.writeText(sourceText.value);
  toast.success("已複製文字到剪貼簿");
  emit("copy", sourceText.value);
};
</script>

<template>
  <InputGroup
    class="relative flex w-1/2 flex-1 flex-col justify-between rounded-l-2xl rounded-r-none border-none bg-transparent! p-4"
  >
    <!-- 頂部：語言標籤與清除按鈕 -->
    <InputGroupAddon align="block-start" class="flex h-7 w-full items-center justify-between p-0">
      <InputGroupText class="text-sm font-medium text-[#8C6D5D]">
        {{ props.languageLabel || "原文" }}
      </InputGroupText>
      <InputGroupButton
        variant="ghost"
        size="icon-xs"
        class="h-6 w-6 rounded-full text-[#8C6D5D] hover:bg-[#4A2D1F] hover:text-[#EAD0C3]"
        @click="handleClear"
      >
        <X class="size-4" />
        <span class="sr-only">清空文字</span>
      </InputGroupButton>
    </InputGroupAddon>

    <!-- 中間：文字輸入區 -->
    <InputGroupTextarea
      v-model="sourceText"
      placeholder="請輸入文字..."
      class="my-3 min-h-[120px] resize-none border-none bg-transparent p-0 text-lg! font-normal text-[#EAD0C3] ring-0 focus-within:ring-0 hover:ring-0 focus-visible:ring-0"
    />

    <!-- 底部右側：功能按鈕膠囊區 -->
    <InputGroupAddon align="block-end" class="flex justify-end p-0">
      <div class="flex items-center gap-1 rounded-full bg-brown-700/60 p-1.5 shadow-sm">
        <InputGroupButton
          variant="ghost"
          size="icon-xs"
          class="hover:text-brown-50 h-7 w-7 rounded-full text-brown-300 hover:bg-brown-800"
          @click="handleSearch"
        >
          <Search class="size-4" />
        </InputGroupButton>
        <InputGroupButton
          variant="ghost"
          size="icon-xs"
          class="h-7 w-7 rounded-full text-brown-300 hover:bg-brown-800"
          @click="handleCopy"
        >
          <Copy class="size-4" />
        </InputGroupButton>
      </div>
    </InputGroupAddon>
  </InputGroup>
</template>