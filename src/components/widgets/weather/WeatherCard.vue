<template>
  <div class="relative flex flex-col gap-0">
    <!-- 概覽 -->
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

    <!-- 詳細資訊 -->
    <div class="grid grid-cols-3 grid-rows-2 gap-0.5 px-5 py-2.5">
      <!-- 濕度 -->
      <WeatherItemContainer>
        <template #icon>
          <Droplet :size="40" :stroke-width="1" class="text-brown-600 opacity-80" />
        </template>
        <p class="text-base font-light text-brown-500">濕度</p>
        <p class="text-2xl font-semibold">
          {{
            getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.relativeHumidity) ||
            "N/A"
          }}%
        </p>
      </WeatherItemContainer>
      <WeatherItemContainer class="col-span-2">
        <template #icon>
          <Wind :size="40" :stroke-width="1" class="text-brown-600 opacity-80" />
        </template>
        <p class="text-base font-light text-brown-500">風</p>
        <p class="text-2xl font-semibold">
          {{
            getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.windSpeed) || "N/A"
          }}級&nbsp;
          {{
            getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.windDirection) || "N/A"
          }}
        </p>
      </WeatherItemContainer>
      <WeatherItemContainer>
        <template #icon>
          <Laugh :size="40" :stroke-width="1" class="text-brown-600 opacity-80" />
        </template>
        <p class="text-base font-light text-brown-500">舒適度指數</p>
        <p class="text-2xl font-semibold">
          {{
            getClosestValueFromMap(
              weatherData?.records[0]?.locations[0]?.comfortIndexDescription,
            ) || "N/A"
          }}
          &nbsp;
          {{ getClosestValueFromMap(weatherData?.records[0]?.locations[0]?.comfortIndex) || "N/A" }}
        </p>
      </WeatherItemContainer>
      <WeatherItemContainer>
        <template #icon>
          <CloudRainWind :size="40" :stroke-width="1" class="text-brown-600 opacity-80" />
        </template>
        <p class="text-base font-light text-brown-500">降雨機率</p>
        <p class="text-2xl font-semibold">
          {{
            getClosestValueFromMap(
              weatherData?.records[0]?.locations[0]?.probabilityOfPrecipitation,
            ) || "N/A"
          }}%
        </p>
      </WeatherItemContainer>
      <a
        href="https://www.cwa.gov.tw/V8/C/W/Town/index.html"
        class="group relative flex items-center justify-between gap-2 overflow-hidden p-2.5 text-brown-500"
      >
        <p class="transition-colors duration-300 group-hover:text-brown-600">檢視更多</p>
      </a>
    </div>

    <!-- 三天天氣概況 -->
    <div class="flex flex-col gap-2.5 px-5 py-3.5">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-white">三天天氣概況</h3>
        <a
          href="https://www.cwa.gov.tw/V8/C/W/week.html"
          class="group relative flex items-center justify-between gap-2 overflow-hidden p-2.5 text-brown-500"
        >
          <p class="transition-colors duration-300 group-hover:text-brown-600">檢視更多</p>
          <ArrowRight
            class="ml-0 transition-all duration-300 group-hover:ml-2 group-hover:text-brown-600"
          />
        </a>
      </div>
      <div class="flex items-center justify-start gap-3"></div>
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
import WeatherItemContainer from "./WeatherItemContainer.vue";
import { ArrowRight, CloudRainWind, Droplet, Laugh, Wind } from "@lucide/vue";

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