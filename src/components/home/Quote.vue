<template>
  <p id="sh-quote-text" class="font-cyly text-subtitle">{{ quote }}</p>
</template>

<style scoped>
#sh-quote-text {
  font-style: normal;
  font-weight: 400;
  line-height: 110%; /* 35.2px */
}
</style>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchQuote } from "@/lib/fetchQuote";

const quote = ref("載入中...");

onMounted(async () => {
  try {
    quote.value = await fetchQuote();
  } catch (error) {
    console.error("Error fetching quote:", error);
  }

  const quoteElement = document.getElementById("sh-quote-text");
  if (quoteElement) {
    quoteElement.addEventListener("click", refreshQuote);
  }
});

// 點擊文本刷新
function refreshQuote() {
  fetchQuote()
    .then((newQuote) => {
      quote.value = newQuote;
    })
    .catch((error) => {
      console.error("Error fetching quote:", error);
    });
}
</script>