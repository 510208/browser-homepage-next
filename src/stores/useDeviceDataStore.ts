import { defineStore } from "pinia";
import { ref } from "vue";
import { type DeviceDataResponse } from "@/types/deviceDataResponse.d";

export const useDeviceDataStore = defineStore("device", () => {
  const deviceData = ref<DeviceDataResponse | null>(null);

  const setDeviceData = (data: DeviceDataResponse) => {
    deviceData.value = data;
  };

  return {
    deviceData,
    setDeviceData,
  };
});
