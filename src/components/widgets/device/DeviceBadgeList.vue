<template>
  <div class="flex flex-wrap gap-2.5">
    <DeviceBadge v-for="badge in badges" :icon-class="badge.iconClass" :key="badge.name">
      <component :is="badge.icon" size="24px" :class="badge.iconClass ?? 'text-brown-500'" />

      <template #content>
        <span class="text-sm font-medium">{{ badge.content }}</span>
      </template>
    </DeviceBadge>
  </div>
</template>

<script setup lang="ts">
import { deviceInfo } from "@/lib/device-info";
import { onMounted, shallowRef } from "vue";

import DeviceBadge from "./DeviceBadge.vue";

import {
  CpuIcon,
  BatteryFullIcon,
  BatteryMediumIcon,
  BatteryLowIcon,
  BatteryWarningIcon,
  BatteryChargingIcon,
  PlugZapIcon,
} from "@lucide/vue";

// 這裡維持原本的 shallowRef 即可
const badges = shallowRef<any[]>([]);

onMounted(async () => {
  try {
    const deviceData = await deviceInfo.fetchDeviceInfo();
    console.log("Device data:", deviceData);

    // CPU狀態
    const cpuUsage = deviceData.cpu.overall_usage_percent;

    // 電池狀態
    let batteryIcon, batteryContent, batteryIconClass;
    if (deviceData.battery) {
      batteryContent = `${deviceData.battery.percent}%`;
      batteryIconClass = "text-brown-500";

      if (deviceData.battery.power_plugged) {
        batteryIcon = BatteryChargingIcon;
      } else {
        const batteryLevel = deviceData.battery.percent;
        if (batteryLevel > 75) {
          batteryIcon = BatteryFullIcon;
        } else if (batteryLevel > 40) {
          batteryIcon = BatteryMediumIcon;
        } else if (batteryLevel > 10) {
          batteryIconClass = "text-yellow-500";
          batteryIcon = BatteryLowIcon;
        } else {
          batteryIconClass = "text-red-500 animate-pulse";
          batteryIcon = BatteryWarningIcon;
        }
      }
    } else {
      batteryContent = "裝置沒有電池";
      batteryIcon = PlugZapIcon;
    }

    badges.value = [
      {
        name: "CPU",
        icon: CpuIcon,
        // 修正 4：給 CPU 一個預設的 iconClass，或者 template 會自動 fallback 到 'text-brown-500'
        iconClass: "text-brown-500",
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
