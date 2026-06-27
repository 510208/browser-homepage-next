<template>
  <DeviceBadge>
    <component :is="batteryIcon" :class="batteryIconClass" :size="24" />

    <template #content>
      <div class="relative flex flex-col gap-0">
        <div class="bg-brown-700 px-5 py-6">
          <div class="flex flex-col items-start gap-2.5">
            <h2 class="text-3xl font-bold text-white">
              {{ batteryData ? `${batteryData.percent}%` : "N/A" }}
            </h2>
            <div class="flex flex-col gap-0.5">
              <p
                class="text-overflow-ellipsis overflow-hidden text-lg whitespace-nowrap text-brown-400"
              >
                {{ batteryStatusText }}
              </p>
            </div>
          </div>
        </div>
      </div>
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

// 定義元件的 Props 屬性
const { batteryData } = defineProps<{
  batteryData: BatteryStatus | undefined;
}>();

// 動態判斷電池狀態文字描述
const batteryStatusText = computed(() => {
  if (!batteryData) {
    return "裝置沒有電池";
  }
  return batteryData.power_plugged ? "外部電源已連接 (充電中)" : "正在使用電池供電";
});

// 動態計算電池圖示元件
const batteryIcon = computed(() => {
  if (!batteryData) {
    return PlugZapIcon;
  }

  if (batteryData.power_plugged) {
    return BatteryChargingIcon;
  }

  const batteryLevel = batteryData.percent;
  if (batteryLevel > 75) {
    return BatteryFullIcon;
  } else if (batteryLevel > 40) {
    return BatteryMediumIcon;
  } else if (batteryLevel > 10) {
    return BatteryLowIcon;
  } else {
    return BatteryWarningIcon;
  }
});

// 動態計算電池圖示顏色樣式類別
const batteryIconClass = computed(() => {
  const baseClass = "transition-colors duration-500";

  if (!batteryData) {
    return `${baseClass} text-gray-400`;
  }

  if (batteryData.power_plugged) {
    return `${baseClass} text-brown-500`;
  }

  const batteryLevel = batteryData.percent;
  if (batteryLevel > 75) {
    return `${baseClass} text-green-400`;
  } else if (batteryLevel > 40) {
    return `${baseClass} text-yellow-400`;
  } else if (batteryLevel > 10) {
    return `${baseClass} text-yellow-400 animate-pulse`;
  } else {
    return `${baseClass} text-red-500 animate-pulse`;
  }
});
</script>
