<script setup lang="ts">
import { Copy, Repeat, X, Check, ChevronDown, Loader2 } from "@lucide/vue";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const props = defineProps<{
  translatedText: string;
  isLoading?: boolean;
}>();

const emit = defineEmits<{
  (e: "clear"): void;
  (e: "swap"): void;
  (e: "copy", text: string): void;
}>();

// 改用 defineModel 接軌 TranslateDialog 的 v-model:target-lang
const targetLang = defineModel<string>("targetLang", { default: "en" });

const languages = [
  { label: "English (US)", value: "en" },
  { label: "繁體中文", value: "zh-TW" },
  { label: "日本語", value: "ja" },
  { label: "한국어", value: "ko" },
];

const handleSelectLanguage = (langCode: string) => {
  targetLang.value = langCode;
};

const handleCopy = () => {
  navigator.clipboard.writeText(props.translatedText);
  emit("copy", props.translatedText);
};
</script>

<template>
  <div
    class="relative flex w-1/2 flex-1 flex-col justify-between rounded-l-none rounded-r-2xl bg-[#4A2D1F] p-4 text-[#EAD0C3]"
  >
    <!-- 頂部：目標語言選單與關閉按鈕 -->
    <header class="flex h-7 w-full items-center justify-between">
      <DropdownMenu>
        <DropdownMenuTrigger
          class="flex items-center gap-1 rounded-md px-1.5 py-1 text-sm font-medium text-[#C29B88] transition-colors hover:bg-[#5C3A29] hover:text-[#EAD0C3]"
        >
          <span>{{ languages.find((l) => l.value === targetLang)?.label || targetLang }}</span>
          <ChevronDown class="size-4 opacity-70" />
        </DropdownMenuTrigger>

        <DropdownMenuContent align="start" class="border-[#5C3A29] bg-[#382014] text-[#EAD0C3]">
          <DropdownMenuItem
            v-for="lang in languages"
            :key="lang.value"
            class="flex items-center justify-between hover:bg-[#4A2D1F] hover:text-[#EAD0C3]"
            @click="handleSelectLanguage(lang.value)"
          >
            <span>{{ lang.label }}</span>
            <Check v-if="targetLang === lang.value" class="size-4 text-[#EAD0C3]" />
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <button
        type="button"
        class="flex h-6 w-6 items-center justify-center rounded-full text-[#C29B88] transition-colors hover:bg-[#5C3A29] hover:text-[#EAD0C3]"
        @click="emit('clear')"
      >
        <X class="size-4" />
      </button>
    </header>

    <!-- 中間：翻譯結果與載入狀態 -->
    <main class="my-3 flex-1 overflow-y-auto">
      <div v-if="props.isLoading" class="flex items-center gap-2 text-[#C29B88]">
        <Loader2 class="size-4 animate-spin" />
        <span>翻譯中...</span>
      </div>
      <p v-else class="text-lg leading-relaxed font-normal whitespace-pre-wrap text-[#EAD0C3]">
        {{ props.translatedText }}
      </p>
    </main>

    <!-- 底部右側：功能按鈕膠囊區 -->
    <footer class="flex justify-end">
      <div class="flex items-center gap-1 rounded-full bg-[#5C3A29] p-1.5 shadow-sm">
        <button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full text-[#EAD0C3] transition-colors hover:bg-[#6E4632]"
          @click="handleCopy"
        >
          <Copy class="size-4" />
        </button>
        <button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full text-[#EAD0C3] transition-colors hover:bg-[#6E4632]"
          @click="emit('swap')"
        >
          <Repeat class="size-4" />
        </button>
      </div>
    </footer>
  </div>
</template>
