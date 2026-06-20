<script setup lang="ts">
import { Clock } from "@/components/widgets/clock";
import { SearchBox } from "@/components/widgets/search-box";
import { Quote } from "@/components/widgets/quote";
import { Avatar } from "@/components/widgets/avatar";
import { Weather } from "@/components/widgets/weather";

import { BottomCenter, RightTop, LeftTop } from "@/components/container";
import Bookmarks from "@/components/widgets/bookmarks/Bookmarks.vue";

import { fetchWeather } from "@/lib/weather/fetchWeather";

import { useWeatherStore } from "@/stores/useWeatherStore";

const weatherStore = useWeatherStore();
weatherStore.setWeatherData(await fetchWeather());
</script>

<template>
  <div id="sh-main" class="fixed top-0 left-0 z-10 h-screen w-screen">
    <BottomCenter>
      <div class="flex flex-col items-center gap-1">
        <Clock />
        <Quote />
      </div>
      <SearchBox />
    </BottomCenter>

    <RightTop>
      <Avatar />
      <Bookmarks class="mt-30" />
    </RightTop>

    <LeftTop>
      <Weather />
    </LeftTop>
  </div>

  <div id="sh-background" class="pointer-events-none fixed top-0 left-0 -z-10 h-screen w-screen">
    <div
      class="absolute inset-0 bg-gradient-to-br from-[#FFFFFF] to-[#555555] mix-blend-soft-light"
    />
    <img
      src="@assets/bg-images/background.png"
      alt="Background"
      class="h-full w-full object-cover"
    />
  </div>
</template>
