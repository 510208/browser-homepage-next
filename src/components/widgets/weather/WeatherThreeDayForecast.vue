<template>
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
</template>

<script setup lang="ts">
import { getWeatherIcon } from "@/lib/weather/utils.ts";
import { computed, ref, onMounted, onUnmounted } from "vue";
import WeatherForecastItem from "./WeatherForecastItem.vue";
import { ArrowRight } from "@lucide/vue";
import type { ForecastItem } from "./WeatherForecastItem.vue";
import { useWeatherStore } from "@/stores/useWeatherStore";

const weatherStore = useWeatherStore();
const weatherData = computed(() => weatherStore.weatherData);

/**
 * 將 ISO 時間字串格式化為易讀的日期與時間
 */
function formatDisplayDate(timeStr: string) {
  try {
    const date = new Date(timeStr);
    // const months = date.getMonth() + 1;
    // const days = date.getDate();
    const hours = String(date.getHours()).padStart(2, "0");
    // const minutes = String(date.getMinutes()).padStart(2, "0");

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
