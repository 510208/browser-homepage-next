<template>
  <div class="flex flex-wrap gap-2.5">
    <BadgeCpu :cpu-data="deviceData?.cpu" />
  </div>
</template>

<script setup lang="ts">
import { deviceInfo } from "@/lib/device-info";
import { onMounted, onUnmounted, ref } from "vue";

import BadgeCpu from "./single-device/BadgeCpu.vue";

import {
  BatteryFullIcon,
  BatteryMediumIcon,
  BatteryLowIcon,
  BatteryWarningIcon,
  BatteryChargingIcon,
  PlugZapIcon,
} from "@lucide/vue";
import type { DeviceDataResponse } from "@/types/deviceDataResponse";

const deviceData = ref<DeviceDataResponse>();
let timerId: ReturnType<typeof setInterval> | null = null;

const updateDeviceInfo = async () => {
  try {
    deviceData.value = await deviceInfo.fetchDeviceInfo();
    console.log("Device data (updated):", deviceData.value);

    // 電池狀態
    let batteryIcon, batteryContent, batteryIconClass;
    if (deviceData.value.battery) {
      batteryContent = `${deviceData.value.battery.percent}%`;
      batteryIconClass = "text-brown-500";

      if (deviceData.value.battery.power_plugged) {
        batteryIcon = BatteryChargingIcon;
      } else {
        const batteryLevel = deviceData.value.battery.percent;
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