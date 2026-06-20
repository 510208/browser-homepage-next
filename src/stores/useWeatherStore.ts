import { defineStore } from "pinia";
import { ref } from "vue";
import type { SimplifiedWeatherResponse } from "@/types/weatherResponse";

export const useWeatherStore = defineStore("weather", () => {
  const weatherData = ref<SimplifiedWeatherResponse | null>(null);

  function setWeatherData(data: SimplifiedWeatherResponse) {
    weatherData.value = data;
  }

  return { weatherData, setWeatherData };
});
