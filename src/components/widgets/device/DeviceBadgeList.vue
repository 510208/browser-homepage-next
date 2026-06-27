<template>
  <div class="flex flex-wrap gap-2.5">
    <BadgeCpu :cpu-data="deviceData?.cpu" />
    <BadgeNetwork :network-data="deviceData?.network" />
    <BadgeBattery :battery-data="deviceData?.battery" />
  </div>
</template>

<script setup lang="ts">
import { deviceInfo } from "@/lib/device-info";
import { onMounted, onUnmounted, ref } from "vue";

import BadgeCpu from "./single-device/BadgeCpu.vue";
import BadgeBattery from "./single-device/BadgeBattery.vue";
import BadgeNetwork from "./single-device/BadgeNetwork.vue";

import type { DeviceDataResponse } from "@/types/deviceDataResponse";

const deviceData = ref<DeviceDataResponse>();
let timerId: ReturnType<typeof setInterval> | null = null;

const updateDeviceInfo = async () => {
  try {
    deviceData.value = await deviceInfo.fetchDeviceInfo();
    console.log("Device data (updated):", deviceData.value);
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
