<template>
  <div class="flex gap-1">
    <img class="size-12" />
  </div>
</template>

<script setup lang="ts">
import { useWeatherStore } from "@/stores/useWeatherStore";

const weatherStore = useWeatherStore();
</script>