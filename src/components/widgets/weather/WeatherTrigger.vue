<template>
  <div class="flex gap-1">
    <img class="size-12" :src="weatherIcon" />
  </div>
</template>

<script setup lang="ts">
import { useWeatherStore } from "@/stores/useWeatherStore";
import { getWeatherIcon, getClosestWeatherCode } from "@/lib/weather/utils";
import type { SimplifiedLocation } from "@/types/weatherResponse";
import { computed, ref, onMounted, onUnmounted } from "vue";
import { fetchWeather } from "@/lib/weather/fetchWeather";

const weatherStore = useWeatherStore();
const currentHour = ref(new Date().getHours());

let updateTimer: number | undefined;

async function updateWeatherAndTimes() {
  try {
    // 呼叫 API 並存入 Pinia Store
    const data = await fetchWeather();
    weatherStore.setWeatherData(data);

    // 同步更新時間，確保日夜狀態正確
    currentHour.value = new Date().getHours();
    // console.log("[Weather] API 與時間已成功自動更新");
  } catch (error) {
    console.error("[Weather] 自動更新失敗:", error);
  }
}

onMounted(async () => {
  await updateWeatherAndTimes();

  updateTimer = window.setInterval(async () => {
    await updateWeatherAndTimes();
  }, 600000);

  // console.log("WeatherTrigger mounted, 輪詢定時器已啟動 ID: ", updateTimer);
});

onUnmounted(() => {
  // 元件銷毀時清除定時器
  if (updateTimer) {
    clearInterval(updateTimer);
    // console.log("WeatherTrigger unmounted, 定時器已清除");
  }
});

const weatherIcon = computed(() => {
  const targetLocation = weatherStore.weatherData?.records[0]?.locations[0];
  const time: "day" | "night" = currentHour.value >= 18 || currentHour.value < 6 ? "night" : "day";

  if (!targetLocation) {
    return getWeatherIcon("01", time);
  }

  const currentCode = getClosestWeatherCode(targetLocation as SimplifiedLocation);
  // console.log("[Weather] currentCode", currentCode);

  return getWeatherIcon(currentCode || "01", time);
});
</script>