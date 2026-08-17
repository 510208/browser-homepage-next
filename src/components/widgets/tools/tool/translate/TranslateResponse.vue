<script setup lang="ts">
import { ref } from "vue";
import { Copy, Repeat, X, Check, ChevronDown } from "@lucide/vue";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const props = defineProps<{
  initialLanguage?: string;
}>();

const emit = defineEmits<{
  (e: "clear"): void;
  (e: "swap"): void;
  (e: "copy", text: string): void;
  (e: "languageChange", lang: string): void;
}>();

// 可選語言列表
const languages = [
  { label: "English (US)", value: "en-US" },
  { label: "English (UK)", value: "en-UK" },
  { label: "繁體中文", value: "zh-TW" },
  { label: "日本語", value: "ja-JP" },
  { label: "한국어", value: "ko-KR" },
];

const selectedLanguage = ref(
  languages.find((l) => l.label === props.initialLanguage) || languages[0],
);
const translatedText = ref("test");

const handleSelectLanguage = (lang: (typeof languages)[number]) => {
  selectedLanguage.value = lang;
  emit("languageChange", lang.value);
};

const handleClear = () => {
  translatedText.value = "";
  emit("clear");
};

const handleCopy = () => {
  navigator.clipboard.writeText(translatedText.value);
  emit("copy", translatedText.value);
};

const handleSwap = () => {
  emit("swap");
};
</script>

<template>
  <div
    class="relative flex min-h-[220px] w-1/2 flex-1 flex-col justify-between rounded-r-2xl bg-brown-700 p-4 text-brown-600"
  >
    <!-- 頂部：目標語言下拉選單與關閉按鈕 -->
    <div class="flex w-full items-center justify-between">
      <DropdownMenu>
        <DropdownMenuTrigger
          class="flex items-center gap-1 rounded-md px-1.5 py-1 text-sm font-medium transition-colors"
        >
          <span>{{ selectedLanguage.label }}</span>
          <ChevronDown class="size-4 opacity-70" />
        </DropdownMenuTrigger>

        <DropdownMenuContent align="start" class="border-[#5C3A29] bg-[#382014] text-[#EAD0C3]">
          <DropdownMenuItem
            v-for="lang in languages"
            :key="lang.value"
            class="flex items-center justify-between hover:bg-[#4A2D1F] hover:text-[#EAD0C3] focus:bg-[#4A2D1F] focus:text-[#EAD0C3]"
            @click="handleSelectLanguage(lang)"
          >
            <span>{{ lang.label }}</span>
            <Check v-if="selectedLanguage.value === lang.value" class="size-4 text-[#EAD0C3]" />
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <button
        type="button"
        class="flex h-6 w-6 items-center justify-center rounded-full text-[#C29B88] transition-colors hover:bg-[#5C3A29] hover:text-[#EAD0C3]"
        @click="handleClear"
      >
        <X class="size-4" />
        <span class="sr-only">Clear translation</span>
      </button>
    </div>

    <!-- 中間：翻譯結果展示區域 -->
    <main class="my-3 flex-1 overflow-y-auto">
      <p class="text-base leading-relaxed font-normal whitespace-pre-wrap text-[#EAD0C3]">
        {{ translatedText }}
      </p>
    </main>

    <!-- 底部右側：功能按鈕膠囊區 -->
    <footer class="flex justify-end">
      <div class="flex items-center gap-1 rounded-full bg-[#5C3A29] p-1.5 shadow-sm">
        <button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full text-[#EAD0C3] transition-colors hover:bg-[#6E4632]"
          title="複製"
          @click="handleCopy"
        >
          <Copy class="size-4" />
          <span class="sr-only">Copy</span>
        </button>
        <button
          type="button"
          class="flex h-7 w-7 items-center justify-center rounded-full text-[#EAD0C3] transition-colors hover:bg-[#6E4632]"
          title="對調語言"
          @click="handleSwap"
        >
          <Repeat class="size-4" />
          <span class="sr-only">Swap language</span>
        </button>
      </div>
    </footer>
  </div>
</template>