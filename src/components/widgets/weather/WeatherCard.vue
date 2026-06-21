<template>
  <div class="relative flex flex-col gap-0">
    <div class="bg-brown-700 px-5 py-6">
      <!-- 天氣圖示 -->
      <div id="sh-weather-icon-wrapper" class="fixed top-0 right-0">
        <img id="sh-weather-icon" class="size-30" :src="weatherIcon" />
      </div>

      <!-- 天氣資訊 -->
      <div class="flex flex-col items-start gap-2.5">
        <h2 class="text-5xl font-bold text-white">
          {{ getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.temperature) || "N/A" }}
          <sup class="text-2xl">°C</sup>
        </h2>
        <div class="flex flex-col gap-0.5">
          <p class="text-xl text-brown-400">
            {{ getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.weather) || "N/A" }}
          </p>
          <p class="text-base text-brown-500">
            體感
            {{
              `${getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.apparentTemperature)}℃` ||
              "N/A"
            }}
            / 露點
            {{ getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.dewPoint) || "N/A" }}℃
            {{
              formatTemperature(
                getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.temperature) || "N/A",
              ) || ""
            }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  getClosestWeatherCode,
  getClosestValueFromMap,
  getWeatherIcon,
  type SimplifiedLocation,
} from "@/lib/weather/utils";
import { useWeatherStore } from "@/stores/useWeatherStore";
import { computed, ref } from "vue";

/**
 * 擷取最高溫度到最低溫度
 * 使用 Regex 的後行斷言 (Lookbehind) ?<=
 */
function formatTemperature(text: string): string | null {
  // 規則：尋找「溫度攝氏」，後面接著一組數字(\d+)，再接著「至」，再接一組數字(\d+)，最後是「度」
  const regex = /溫度攝氏(\d+)至(\d+)度/;
  const match = text.match(regex);

  // 如果沒有匹配到（代表它是單一溫度如"32度"，或者根本沒溫度資料）
  if (!match) {
    return null;
  }

  // match[1] 是第一個括號抓到的字串 (最低溫)
  // match[2] 是第二個括號抓到的字串 (最高溫)
  const lowTemp = match[1];
  const highTemp = match[2];

  // 組合回傳你想要的格式
  return ` / 最高 ${highTemp}℃ / 最低 ${lowTemp}℃`;
}

const weatherStore = useWeatherStore();
const currentHour = ref(new Date().getHours());

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

const weatherData = computed(() => weatherStore.weatherData);
</script>

<style scoped>
#sh-weather-icon-wrapper {
  background:
    radial-gradient(26.68% 26.68% at 60% 39.58%, #f3712d 0%, rgba(154, 94, 76, 0) 90%),
    radial-gradient(50% 50% at 50% 50%, rgba(255, 255, 255, 0.4) 0%, rgba(153, 153, 153, 0) 90%);
}
</style>