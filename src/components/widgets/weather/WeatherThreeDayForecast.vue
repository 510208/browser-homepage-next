<template>
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
        class="relative flex scrollbar-none gap-0 overflow-x-auto pb-4"
        id="sh-weather-forecast-wrapper"
      >
        <div
          v-if="threeDayForecast.length > 0"
          class="pointer-events-none absolute bottom-0 left-0 z-0 h-24"
          :style="{ width: chartCanvasWidth + 'px' }"
        >
          <ChartContainer :config="chartConfig" class="h-full w-full">
            <VisXYContainer :data="threeDayForecast" :margin="chartMargin" :y-domain="yDomain">
              <VisArea
                :x="(d: ForecastItem) => d.timeKey"
                :y="(d: ForecastItem) => parseFloat(d.temperature)"
                color="var(--chart-temperature)"
                :opacity="0.15"
              />

              <VisLine
                :x="(d: ForecastItem) => d.timeKey"
                :y="(d: ForecastItem) => parseFloat(d.temperature)"
                color="var(--chart-temperature)"
                :stroke-width="2"
              />
            </VisXYContainer>
          </ChartContainer>
        </div>

        <WeatherForecastItem
          v-for="forecast in threeDayForecast"
          :key="forecast.timeKey"
          :forecast="forecast"
          class="z-10 min-w-[76px] flex-1"
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
import { computed, ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import WeatherForecastItem from "./WeatherForecastItem.vue";
import { ArrowRight } from "@lucide/vue";
import type { ForecastItem } from "./WeatherForecastItem.vue";
import { useWeatherStore } from "@/stores/useWeatherStore";

// 引入 Shadcn / Unovis 圖表組件
import { VisXYContainer, VisLine, VisArea } from "@unovis/vue";
import { ChartContainer, type ChartConfig } from "@/components/ui/chart";

const weatherStore = useWeatherStore();
const weatherData = computed(() => weatherStore.weatherData);

// 響應式儲存滾動容器實際內襯總寬度
const wrapperScrollWidth = ref(0);

/**
 * 將 ISO 時間字串格式化為易讀的日期與時間
 */
function formatDisplayDate(timeStr: string) {
  try {
    const date = new Date(timeStr);
    const hours = String(date.getHours()).padStart(2, "0");
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

const forecastWrapper = ref<HTMLElement | null>(null);
const showLeftMask = ref(false);
const showRightMask = ref(false);

/**
 * 計算並更新左右遮罩的顯示狀態與實際總寬度
 */
function updateMasks() {
  if (!forecastWrapper.value) return;

  const { scrollLeft, scrollWidth, clientWidth } = forecastWrapper.value;

  showLeftMask.value = scrollLeft > 1;
  showRightMask.value = scrollLeft + clientWidth < scrollWidth - 1;

  // 同步當前滾動容器內部的總寬度
  wrapperScrollWidth.value = scrollWidth;
}

let resizeObserver: ResizeObserver | null = null;

onMounted(() => {
  if (forecastWrapper.value) {
    forecastWrapper.value.addEventListener("scroll", updateMasks);

    resizeObserver = new ResizeObserver(() => {
      updateMasks();
    });
    resizeObserver.observe(forecastWrapper.value);

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

// 當非同步資料載入並完成 DOM 渲染後，重新觸發尺寸狀態計算
watch(
  () => threeDayForecast.value,
  () => {
    nextTick(() => {
      updateMasks();
    });
  },
  { deep: true },
);

/**
 * 圖表寬度映射綁定
 */
const chartCanvasWidth = computed(() => {
  return wrapperScrollWidth.value || 0;
});

/**
 * Shadcn 圖表色彩配置設定
 */
const chartConfig = {
  temperature: {
    label: "溫度",
    color: "#f3712d",
  },
} satisfies ChartConfig;

/**
 * 計算屬性：動態調整 Y 軸域，確保折線置中
 */
const yDomain = computed<[number, number]>(() => {
  const dataset = threeDayForecast.value;
  if (dataset.length === 0) return [0, 40];

  const temps = dataset.map((d) => parseFloat(d.temperature)).filter((t) => !isNaN(t));

  if (temps.length === 0) return [0, 40];

  const min = Math.min(...temps);
  const max = Math.max(...temps);

  // 邊界上下留空 2 度，防止拐點貼緊圖表上下邊緣
  return [min - 2, max + 2];
});

/**
 * 計算屬性：調整邊距補償
 * 左右內縮半個元件的寬度，修正 Unovis 起始點與 WeatherForecastItem 置中位置對齊
 */
const chartMargin = computed(() => {
  const dataset = threeDayForecast.value;
  if (dataset.length === 0 || chartCanvasWidth.value === 0) {
    return { left: 0, right: 0, top: 20, bottom: 0 };
  }
  const itemWidth = chartCanvasWidth.value / dataset.length;
  const halfItemWidth = itemWidth / 2;

  return {
    left: halfItemWidth,
    right: halfItemWidth,
    top: 20,
    bottom: 0,
  };
});
</script>

<style scoped>
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

/* 將色彩屬性注入全域 CSS 變數，供內部 Unovis 圖表模組進行讀取 */
:thin-root,
:host,
::v-deep(*) {
  --chart-temperature: #f3712d;
}
</style>
