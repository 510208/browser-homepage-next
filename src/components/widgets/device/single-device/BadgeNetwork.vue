<template>
  <DeviceCard>
    <div class="relative h-6 w-6">
      <WifiIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === 'Wi-Fi' ? 'opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />
      <NetworkIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === '有線網路' ? 'opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />
      <GlobeOffIcon
        :style="iconStyle"
        :class="[
          'absolute top-0 left-0 transition-all duration-500',
          currentActiveIcon === '沒有連線' ? 'animate-pulse opacity-100' : 'opacity-0',
        ]"
        :size="24"
      />
    </div>

    <template #content>
      <div class="relative flex flex-col gap-0">
        <div class="bg-brown-700 px-5 py-6">
          <div class="flex flex-col items-start gap-2.5">
            <h2 class="text-3xl font-bold text-white">
              {{ networkData?.type || "沒有連線" }}
            </h2>
            <div class="flex flex-col gap-0.5">
              <p
                class="text-overflow-ellipsis overflow-hidden text-lg whitespace-nowrap text-brown-400"
              >
                {{ networkName }}
              </p>
            </div>
          </div>
        </div>

        <div class="max-h-48 overflow-y-auto px-5 pt-2.5 pb-5">
          <span class="block text-base font-medium text-gray-400">累計數據流量</span>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-0.5">
              <span class="text-base font-medium text-gray-500">累計發送</span>
              <span class="font-mono text-lg font-semibold text-gray-300">
                {{ formatBytes(networkData?.bytes_sent) }}
              </span>
            </div>

            <div class="flex flex-col gap-0.5">
              <span class="text-base font-medium text-gray-500">累計接收</span>
              <span class="font-mono text-lg font-semibold text-gray-300">
                {{ formatBytes(networkData?.bytes_recv) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DeviceCard>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { NetworkStatus } from "@/types/deviceDataResponse";
import DeviceCard from "../DeviceCard.vue";
import { WifiIcon, NetworkIcon, GlobeOffIcon } from "@lucide/vue";

// 定義色碼常數
const COLORS = {
  text_red_500: "#ef4444",
  text_brown_500: "#8b5a2b",
};

// 定義元件的 Props 屬性
const { networkData } = defineProps<{
  networkData: NetworkStatus | null | undefined;
}>();

const networkName = computed(() => {
  if (!networkData || networkData.type === "沒有連線") {
    return "未登錄網路介面";
  }
  return networkData.name || "未知網路名稱";
});

// 計算當前應該顯示的圖示標籤名稱
const currentActiveIcon = computed(() => {
  if (!networkData || networkData.type === "沒有連線") {
    return "沒有連線";
  }
  if (networkData.type === "Wi-Fi") {
    return "Wi-Fi";
  }
  if (networkData.type === "有線網路") {
    return "有線網路";
  }
  // 若有其他自訂網路類型，預設歸類至有線圖示
  return "有線網路";
});

// 計算當前的顏色，提供給 CSS 變數做 v-bind 綁定
const currentIconColor = computed(() => {
  if (!networkData || networkData.type === "沒有連線") {
    return COLORS.text_red_500;
  }

  return COLORS.text_brown_500;
});

// 封裝 Style 屬性
const iconStyle = computed(() => {
  return {
    color: currentIconColor.value,
  };
});

// 資料量單位轉換函式（Bytes 轉為合適的 GB/MB/KB 單位）
const formatBytes = (bytes: number | undefined): string => {
  if (bytes === undefined || bytes === null || isNaN(bytes)) return "0 Bytes";
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};
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