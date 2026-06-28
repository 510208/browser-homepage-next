<template>
  <DeviceBadge>
    <div class="relative h-6 w-6">
      <!-- BatteryFullIcon -->
      <BatteryFullIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Full' ? 'opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />

      <!-- BatteryMediumIcon -->
      <BatteryMediumIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Medium' ? 'opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />

      <!-- BatteryLowIcon -->
      <BatteryLowIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Low' ? 'animate-pulse opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />

      <!-- BatteryWarningIcon -->
      <BatteryWarningIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Warning' ? 'animate-bounce opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />

      <!-- BatteryChargingIcon -->
      <BatteryChargingIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Charging' ? 'animate-pulse opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />

      <!-- PlugZapIcon -->
      <PlugZapIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'NoBattery' ? 'opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />
    </div>

    <template #content>
      {{ batteryStatusText }}{{ batteryData ? `，${batteryData.percent}%` : "" }}
    </template>
  </DeviceBadge>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { BatteryStatus } from "@/types/deviceDataResponse";
import DeviceBadge from "../DeviceBadge.vue";
import {
  BatteryFullIcon,
  BatteryMediumIcon,
  BatteryLowIcon,
  BatteryWarningIcon,
  BatteryChargingIcon,
  PlugZapIcon,
} from "@lucide/vue";

// 定義色碼常數
const COLORS = {
  text_green_400: "#4ade80",
  text_yellow_400: "#facc15",
  text_red_500: "#ef4444",
  text_brown_500: "#8b5a2b",
  text_gray_400: "#9ca3af",
};

// 定義元件的 Props 屬性
const { batteryData } = defineProps<{
  batteryData: BatteryStatus | null | undefined;
}>();

// 動態判斷電池狀態文字描述
const batteryStatusText = computed(() => {
  if (!batteryData || batteryData.percent === undefined) {
    return "裝置沒有電池";
  }
  return batteryData.power_plugged ? "外部電源已連接 (充電中)" : "正在使用電池供電";
});

// 計算當前應該顯示的圖示標籤名稱
const currentActiveIcon = computed(() => {
  if (!batteryData || batteryData.percent === undefined) {
    return "NoBattery";
  }

  if (batteryData.power_plugged) {
    return "Charging";
  }

  const batteryLevel = batteryData.percent;
  if (batteryLevel > 75) {
    return "Full";
  } else if (batteryLevel > 40) {
    return "Medium";
  } else if (batteryLevel > 10) {
    return "Low";
  } else {
    return "Warning";
  }
});

// 計算當前的顏色，提供給 CSS 變數做 v-bind 綁定
const currentIconColor = computed(() => {
  if (!batteryData || batteryData.percent === undefined) {
    // 無電池資料，對應原本的 text-gray-400 十六進位值
    return COLORS.text_gray_400;
  }

  // if (batteryData.power_plugged) {
  //   // 充電中，對應您自定義的 brown-500 十六進位值（此處以範例色值代入，可依專案實際變數修改）
  //   return COLORS.text_brown_500;
  // }

  const batteryLevel = batteryData.percent;
  if (batteryLevel > 75) {
    // 對應 text-green-400
    return COLORS.text_green_400;
  } else if (batteryLevel > 40) {
    // 對應 text-yellow-400
    return COLORS.text_yellow_400;
  } else if (batteryLevel > 10) {
    // 對應 text-yellow-400
    return COLORS.text_yellow_400;
  } else {
    // 對應 text-red-500
    return COLORS.text_red_500;
  }
});

// 封裝 Style 屬性，確保過渡動畫包含 color 與 opacity
const iconStyle = computed(() => {
  return {
    color: currentIconColor.value,
  };
});
</script>

<style scoped>
/* 使用 style 標籤配合 v-bind 綁定動態顏色，並定義平滑過渡效果 */
.transition-all {
  color: v-bind(currentIconColor);
  transition:
    opacity 500ms ease-in-out,
    color 500ms ease-in-out;
}
</style>