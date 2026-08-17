<template>
  <div
    class="flex w-full max-w-2xl flex-nowrap items-stretch gap-0 overflow-hidden rounded-2xl border border-[#4A2D1F]"
  >
    <TranslateSource />
    <TranslateResponse />
  </div>
</template>

<script setup lang="ts">
import TranslateResponse from "./TranslateResponse.vue";
import TranslateSource from "./TranslateSource.vue";
</script>