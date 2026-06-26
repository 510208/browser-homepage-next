<template>
  <div class="flex flex-wrap gap-2.5">
    <DeviceBadge v-for="badge in badges" :key="badge.name" :iconClass="badge.iconClass">
      <template #icon>
        <component :is="badge.icon" size="24px" class="text-brown-500" />
      </template>
    </DeviceBadge>
  </div>
</template>

<script setup lang="ts">
import { deviceInfo } from "@/lib/device-info";
import { onMounted, ref } from "vue";

import DeviceBadge from "./DeviceBadge.vue";

import {
  CpuIcon,
  BatteryFullIcon, // 適用於有電池且滿電的情況
  BatteryMediumIcon, // 適用於有電池且中等電量的情況
  BatteryLowIcon, // 適用於有電池且低電量的情況
  BatteryWarningIcon, // 適用於有電池且電量極低的情況
  BatteryChargingIcon, // 適用於有電池且正在充電的情況
  PlugZapIcon, // 適用於有線電源的情況
} from "@lucide/vue";

const badges = ref<any[]>([]);

onMounted(async () => {
  try {
    const deviceData = await deviceInfo.fetchDeviceInfo();

    // CPU狀態
    const cpuUsage = deviceData.cpu.overall_usage_percent;

    // 電池狀態
    // 選擇適當的電池圖標根據電池狀態
    let batteryIcon, batteryContent, batteryIconClass;
    if (deviceData.battery) {
      // 如果有電池，根據電池狀態選擇圖標
      batteryContent = `${deviceData.battery.percent}%`;
      batteryIconClass = "text-brown-500"; // 設定圖標預設顏色

      if (deviceData.battery.power_plugged) {
        // 正在充電
        batteryIcon = BatteryChargingIcon;
      } else {
        const batteryLevel = deviceData.battery.percent;
        if (batteryLevel > 75) {
          // 高電量
          batteryIcon = BatteryFullIcon;
        } else if (batteryLevel > 40) {
          // 中等電量
          batteryIcon = BatteryMediumIcon;
        } else if (batteryLevel > 10) {
          // 低電量
          batteryIconClass = "text-yellow-500"; // 設定圖標為黃色
          batteryIcon = BatteryLowIcon;
        } else {
          // 極低電量
          batteryIconClass = "text-red-500 animate-pulse"; // 設定圖標為紅色並添加脈衝動畫
          batteryIcon = BatteryWarningIcon;
        }
      }
    } else {
      // 如果沒有電池，使用有線電源圖標
      batteryContent = "裝置沒有電池";
      batteryIcon = PlugZapIcon;
    }

    badges.value = [
      {
        name: "CPU",
        icon: CpuIcon,
        content: `${cpuUsage.toFixed(2)}%`,
      },
      {
        name: "Battery",
        icon: batteryIcon,
        iconClass: batteryIconClass,
        content: batteryContent,
      },
    ];
  } catch (error) {
    console.error("Failed to fetch device info:", error);
  }
});
</script>
