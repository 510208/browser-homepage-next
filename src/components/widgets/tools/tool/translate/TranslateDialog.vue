<template>
  <div
    class="flex w-full max-w-2xl flex-nowrap items-stretch gap-0 overflow-hidden rounded-2xl border border-[#4A2D1F]"
  >
    <TranslateSource v-model:source-text="sourceText" @clear="handleClear" />
    <TranslateResponse
      v-model:target-lang="targetLang"
      :translated-text="translatedText"
      :is-loading="isLoading"
      @clear="handleClear"
      @swap="handleSwap"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import TranslateResponse from "./TranslateResponse.vue";
import TranslateSource from "./TranslateSource.vue";

const sourceText = ref("");
const targetLang = ref("en");
const translatedText = ref("");
const isLoading = ref(false);

// 使用 Lingva API 進行翻譯作業
const translateWithLingva = async (
  text: string,
  sourceLang = "auto",
  targetLangCode = "en",
): Promise<string> => {
  const encodedText = encodeURIComponent(text);
  // Lingva Endpoint API URL 格式修正與拼接
  const url = `https://lingva.ml/api/v1/${sourceLang}/${targetLangCode}/${encodedText}`;

  const response = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`HTTP 錯誤！狀態碼: ${response.status}`);
  }

  const data = await response.json();
  return data.translation;
};

// 執行翻譯作業的核心邏輯
const executeTranslate = async () => {
  if (!sourceText.value.trim()) {
    translatedText.value = "";
    return;
  }

  isLoading.value = true;
  try {
    const result = await translateWithLingva(sourceText.value, "auto", targetLang.value);
    translatedText.value = result;
  } catch (error) {
    console.error("Lingva 翻譯發生錯誤:", error);
  } finally {
    isLoading.value = false;
  }
};

// 監聽輸入內容，200ms 防抖觸發 API 請求
watchDebounced(
  sourceText,
  () => {
    executeTranslate();
  },
  { debounce: 200, maxWait: 500 },
);

// 切換目標語言時立即重新翻譯
watch(targetLang, () => {
  executeTranslate();
});

// 清空內容
const handleClear = () => {
  sourceText.value = "";
  translatedText.value = "";
};

// 對調語言與內文
const handleSwap = () => {
  if (translatedText.value) {
    sourceText.value = translatedText.value;
  }
};
</script>