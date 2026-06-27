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
import { toast } from "vue-sonner";

const deviceData = ref<DeviceDataResponse>();
let timerId: ReturnType<typeof setInterval> | null = null;

const updateDeviceInfo = async () => {
  try {
    deviceData.value = await deviceInfo.fetchDeviceInfo();
    console.log("Device data (updated):", deviceData.value);
  } catch (error) {
    console.error("Failed to fetch device info:", error);
    throw error;
  }
};

onMounted(async () => {
  try {
    await updateDeviceInfo();
  } catch (error) {
    toast.error("無法取得裝置資訊，請確認本地端服務是否啟動。\n詳情請查看瀏覽器控制台。");
    console.warn(
      "請檢查本地端服務（ https://github.com/510208/browser-homepage-next/tree/main/server ）是否已正確的安裝並啟動。\n若已啟動，請向上檢查可能的問題，或前往儲存庫建立Issue。\n若這個問題是有意的，請在 src/App.vue 中移除或停用 <DeviceBadgeList /> 元件。",
    );
  }

  timerId = setInterval(updateDeviceInfo, 3000);
});

onUnmounted(() => {
  if (timerId) {
    clearInterval(timerId);
    timerId = null;
  }
});
</script>
