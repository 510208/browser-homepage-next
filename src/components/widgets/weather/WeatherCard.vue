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
          class="group relative flex items-center justify-between gap-2 overflow-hidden rounded-md bg-transparent px-2.5 py-1 text-brown-500 transition-colors duration-300 hover:bg-brown-700/50"
        >
          <p class="transition-colors duration-300 group-hover:text-brown-600">檢視更多</p>
          <ArrowRight
            class="ml-0 transition-all duration-300 group-hover:ml-2 group-hover:text-brown-600"
          />
        </a>
      </div>
      <div class="relative w-full">
        <div
          ref="forecastWrapper"
          class="flex scrollbar-none gap-3 overflow-x-auto"
          id="sh-weather-forecast-wrapper"
        >
          <WeatherForecastItem
            v-for="forecast in threeDayForecast"
            :key="forecast.timeKey"
            :forecast="forecast"
          />
        </div>

        <div
          :data-show="showLeftMask"
          id="sh-weather-forecast-left-mask"
          class="sh-shadow-mask pointer-events-none absolute top-0 left-0 h-full w-12 bg-gradient-to-r from-brown-800 to-transparent transition-opacity duration-200"
        ></div>
        <div
          :data-show="showRightMask"
          id="sh-weather-forecast-right-mask"
          class="sh-shadow-mask pointer-events-none absolute top-0 right-0 h-full w-12 bg-gradient-to-l from-brown-800 to-transparent transition-opacity duration-200"
        ></div>
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
import { computed, onMounted, onUnmounted, ref } from "vue";

import WeatherItemContainer from "./WeatherItemContainer.vue";
import WeatherForecastItem from "./WeatherForecastItem.vue";
import type { ForecastItem } from "./WeatherForecastItem.vue";

import { ArrowRight, CloudRainWind, Droplet, Laugh, Wind } from "@lucide/vue";

/**
 * 擷取最高溫度到最低溫度
 * 使用 Regex 的後行斷言 (Lookbehind) ?<=
 */
function formatTemperature(text: string): string | null {
  const regex = /溫度攝氏(\d+)至(\d+)度/;
  const match = text.match(regex);

  if (!match) {
    return null;
  }

  const lowTemp = match[1];
  const highTemp = match[2];

  return ` / 最高 ${highTemp}℃ / 最低 ${lowTemp}℃`;
}

/**
 * 將 ISO 時間字串格式化為易讀的日期與時間
 */
function formatDisplayDate(timeStr: string) {
  try {
    const date = new Date(timeStr);
    // const months = date.getMonth() + 1;
    // const days = date.getDate();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const weekdayMap = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"];
    const weekday = weekdayMap[date.getDay()];

    return {
      date: `${weekday}`,
      time: `${hours}時`,
      hourValue: date.getHours(),
    };
  } catch (e) {
    return { date: "未知日期", time: "--:--", hourValue: 12 };
  }
}

const weatherStore = useWeatherStore();
const currentHour = ref(new Date().getHours());

const weatherData = computed(() => weatherStore.weatherData);

const weatherIcon = computed(() => {
  const targetLocation = weatherStore.weatherData?.records[0]?.locations[0];
  const time: "day" | "night" = currentHour.value >= 18 || currentHour.value < 6 ? "night" : "day";

  if (!targetLocation) {
    return getWeatherIcon("01", time);
  }

  const currentCode = getClosestWeatherCode(targetLocation as SimplifiedLocation);

  return getWeatherIcon(currentCode || "01", time);
});

/**
 * 計算屬性：整合、排序並篩選未來三天的預報資料
 */
const threeDayForecast = computed(() => {
  const targetLocation = weatherData.value?.records[0]?.locations[0];
  if (!targetLocation) {
    return [];
  }

  const tempMap = targetLocation.temperature || {};
  const weatherMap = targetLocation.weather || {};
  const codeMap = targetLocation.weatherCode || {};

  const allTimeKeys = Array.from(
    new Set([...Object.keys(tempMap), ...Object.keys(weatherMap), ...Object.keys(codeMap)]),
  ).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

  const nowTime = Date.now();
  const threeDaysMaxTime = nowTime + 3 * 24 * 60 * 60 * 1000;

  return allTimeKeys
    .filter((timeKey) => {
      const itemTime = new Date(timeKey).getTime();
      return itemTime >= nowTime && itemTime <= threeDaysMaxTime;
    })
    .map((timeKey): ForecastItem => {
      const formatInfo = formatDisplayDate(timeKey);
      const period: "day" | "night" =
        formatInfo.hourValue >= 18 || formatInfo.hourValue < 6 ? "night" : "day";
      const currentCode = codeMap[timeKey] || "01";

      return {
        timeKey,
        displayDate: formatInfo.date,
        displayTime: formatInfo.time,
        temperature: tempMap[timeKey] || "N/A",
        weather: weatherMap[timeKey] || "N/A",
        icon: getWeatherIcon(currentCode, period),
      };
    });
});

// 偵測sh-weather-forecast-wrapper的捲動位置，並顯示或隱藏左右遮罩
const forecastWrapper = ref<HTMLElement | null>(null);
const showLeftMask = ref(false);
const showRightMask = ref(false);

/**
 * 計算並更新左右遮罩的顯示狀態
 */
function updateMasks() {
  if (!forecastWrapper.value) return;

  const { scrollLeft, scrollWidth, clientWidth } = forecastWrapper.value;

  // 當捲動距離大於 0 時，顯示左側淡出遮罩
  showLeftMask.value = scrollLeft > 1;

  // 當總寬度大於視窗寬度，且尚未捲動到最右端時，顯示右側淡出遮罩
  // 加上 1 像素的緩衝以避免部分瀏覽器因為浮點數四捨五入導致計算不精準
  showRightMask.value = scrollLeft + clientWidth < scrollWidth - 1;
}

// 建立尺寸監聽器，捕捉內容因資料載入或視窗縮放帶來的寬度變化
let resizeObserver: ResizeObserver | null = null;

onMounted(() => {
  if (forecastWrapper.value) {
    // 綁定原生滾動事件
    forecastWrapper.value.addEventListener("scroll", updateMasks);

    // 初始化 ResizeObserver
    resizeObserver = new ResizeObserver(() => {
      updateMasks();
    });
    resizeObserver.observe(forecastWrapper.value);

    // 執行初始檢查
    updateMasks();
  }
});

onUnmounted(() => {
  if (forecastWrapper.value) {
    forecastWrapper.value.removeEventListener("scroll", updateMasks);
  }
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<style scoped>
#sh-weather-icon-wrapper {
  background:
    radial-gradient(26.68% 26.68% at 60% 39.58%, #f3712d 0%, rgba(154, 94, 76, 0) 90%),
    radial-gradient(50% 50% at 50% 50%, rgba(255, 255, 255, 0.4) 0%, rgba(153, 153, 153, 0) 90%);
}

#sh-weather-forecast-wrapper {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

.sh-shadow-mask[data-show="false"] {
  opacity: 0;
}

.sh-shadow-mask[data-show="true"] {
  opacity: 1;
}
</style>
