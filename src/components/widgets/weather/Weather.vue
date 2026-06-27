<template>
  <HoverCard v-model:open="openWeatherCard" :openDelay="50" :closeDelay="200">
    <HoverCardTrigger>
      <WeatherTrigger />
    </HoverCardTrigger>
    <HoverCardContent class="w-[400px] overflow-hidden px-0 py-0" align="start">
      <WeatherCard />
    </HoverCardContent>
  </HoverCard>
</template>

<script setup lang="ts">
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { WeatherCard, WeatherTrigger } from "./index";
import hotkeys from "hotkeys-js";
import { ref, onMounted, onUnmounted } from "vue";

const openWeatherCard = ref<boolean>(false);

onMounted(() => {
  hotkeys("w", () => {
    // 檢查天氣卡片是否已開啟，如果已開啟則不動作，否則開啟並在5秒後關閉
    if (!openWeatherCard.value) {
      openWeatherCard.value = true;
      setTimeout(() => {
        openWeatherCard.value = false;
      }, 5000);
    }
  });
});

onUnmounted(() => {
  hotkeys.unbind();
});
</script>