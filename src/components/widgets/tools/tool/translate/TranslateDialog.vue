<template>
  <div
    class="flex w-full max-w-2xl flex-nowrap items-stretch gap-0 overflow-hidden rounded-2xl border border-brown-800 bg-brown-900"
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
import JsGoogleTranslateFree from "@kreisler/js-google-translate-free";
import TranslateResponse from "./TranslateResponse.vue";
import TranslateSource from "./TranslateSource.vue";

const sourceText = ref("");
const targetLang = ref("en");
const translatedText = ref("");
const isLoading = ref(false);

// 執行翻譯作業的核心邏輯
const executeTranslate = async () => {
  if (!sourceText.value.trim()) {
    translatedText.value = "";
    return;
  }

  isLoading.value = true;
  try {
    const translation = await JsGoogleTranslateFree.translate({
      to: targetLang.value as "en" | "zh-TW" | "ja" | "ko",
      text: sourceText.value,
    });

    translatedText.value = translation;
  } catch (error) {
    console.error("JsGoogleTranslateFree 翻譯發生錯誤:", error);
  } finally {
    isLoading.value = false;
  }
};

// 監聽輸入內容變動，200ms 防抖觸發翻譯 API
watchDebounced(
  sourceText,
  () => {
    executeTranslate();
  },
  { debounce: 200, maxWait: 500 },
);

// 當切換目標語言時，立即重新發送翻譯請求
watch(targetLang, () => {
  executeTranslate();
});

// 清空內容
const handleClear = () => {
  sourceText.value = "";
  translatedText.value = "";
};

// 對調語言與文字
const handleSwap = () => {
  if (translatedText.value) {
    [sourceText.value, translatedText.value] = [translatedText.value, sourceText.value];
  }
};
</script>
