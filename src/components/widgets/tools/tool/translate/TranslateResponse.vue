<script setup lang="ts">
import { Copy, Repeat, X, Check, ChevronDown, Loader2 } from "@lucide/vue";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { toast } from "vue-sonner";

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
  toast.success("已複製文字到剪貼簿");
  emit("copy", props.translatedText);
};
</script>

<template>
  <div
    class="relative flex w-1/2 flex-1 flex-col justify-between rounded-l-none rounded-r-2xl bg-brown-800 p-4 text-brown-100"
  >
    <!-- 頂部：目標語言選單與關閉按鈕 -->
    <header class="flex h-7 w-full items-center justify-between">
      <DropdownMenu>
        <DropdownMenuTrigger
          class="flex items-center gap-1 rounded-md px-1.5 py-1 text-sm font-medium text-brown-500 transition-colors hover:bg-brown-700 hover:text-brown-100"
        >
          <span>{{ languages.find((l) => l.value === targetLang)?.label || targetLang }}</span>
          <ChevronDown class="size-4 opacity-70" />
        </DropdownMenuTrigger>

        <DropdownMenuContent align="start" class="border-brown-700 bg-brown-800 text-brown-100">
          <DropdownMenuItem
            v-for="lang in languages"
            :key="lang.value"
            class="flex items-center justify-between hover:bg-brown-700 hover:text-brown-100"
            @click="handleSelectLanguage(lang.value)"
          >
            <span>{{ lang.label }}</span>
            <Check v-if="targetLang === lang.value" class="size-4 text-brown-100" />
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <Button
        type="button"
        variant="ghost"
        class="flex h-6 w-6 items-center justify-center rounded-full text-brown-400 transition-colors hover:bg-brown-700 hover:text-brown-100"
        @click="emit('clear')"
      >
        <X class="mr-8 size-4" />
      </Button>
    </header>

    <!-- 中間：翻譯結果與載入狀態 -->
    <main class="my-3 flex-1 overflow-y-auto">
      <div v-if="props.isLoading" class="flex items-center gap-2 text-brown-400">
        <Loader2 class="size-4 animate-spin" />
        <span>翻譯中...</span>
      </div>
      <p v-else class="text-lg leading-relaxed font-normal whitespace-pre-wrap text-brown-100">
        {{ props.translatedText }}
      </p>
    </main>

    <!-- 底部右側：功能按鈕膠囊區 -->
    <footer class="flex justify-end">
      <div class="flex items-center gap-1 rounded-full bg-brown-700 p-1.5 shadow-sm">
        <Button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full"
          @click="handleCopy"
          variant="ghost"
        >
          <Copy class="size-4" />
        </Button>
        <Button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full"
          variant="ghost"
          @click="emit('swap')"
        >
          <Repeat class="size-4" />
        </Button>
      </div>
    </footer>
  </div>
</template>
