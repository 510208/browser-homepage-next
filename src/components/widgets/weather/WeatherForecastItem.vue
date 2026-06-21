<template>
  <div class="flex flex-col items-center justify-center gap-4 py-4">
    <div class="flex items-center justify-center">
      <img :src="forecast.icon" :alt="forecast.weather" class="size-12 object-contain" />
    </div>

    <div class="items-left flex flex-col gap-1">
      <span class="text-xl font-semibold tracking-tight text-white/90">
        {{ forecast.temperature }}°C
      </span>

      <span class="text-sm font-normal text-brown-400/80">
        {{ forecast.displayDate }}<br />
        {{ forecast.displayTime }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface ForecastItem {
  timeKey: string;
  displayDate: string;
  displayTime: string;
  temperature: string;
  weather: string;
  icon: string;
}

defineProps<{
  forecast: ForecastItem;
}>();
</script>