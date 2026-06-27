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
import { onMounted, onUnmounted, shallowRef } from "vue";

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

const badges = shallowRef<any[]>([]);
let timerId: ReturnType<typeof setInterval> | null = null;

const updateDeviceInfo = async () => {
  try {
    const deviceData = await deviceInfo.fetchDeviceInfo();
    console.log("Device data (updated):", deviceData);

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
          // >= 75%
          batteryIconClass = "text-green-400";
          batteryIcon = BatteryFullIcon;
        } else if (batteryLevel > 40) {
          // 75% - 40%
          batteryIconClass = "text-yellow-400";
          batteryIcon = BatteryMediumIcon;
        } else if (batteryLevel > 10) {
          // 40% - 10%
          batteryIconClass = "text-yellow-400 animate-pulse";
          batteryIcon = BatteryLowIcon;
        } else {
          // <= 10%
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
};

onMounted(async () => {
  await updateDeviceInfo();

  timerId = setInterval(updateDeviceInfo, 3000);
});

onUnmounted(() => {
  if (timerId) {
    clearInterval(timerId);
    timerId = null;
  }
});
</script>