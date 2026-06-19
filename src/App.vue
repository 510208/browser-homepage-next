<script setup lang="ts">
import { Clock } from "@/components/widgets/clock";
import { SearchBox } from "@/components/widgets/search-box";
import { Quote } from "@/components/widgets/quote";
import BottomCenter from "@/components/container/BottomCenter.vue";
import RightTop from "./components/container/RightTop.vue";
</script>

<template>
  <div id="sh-main" class="h-screen w-screen bg-transparent">
    <BottomCenter>
      <div class="flex flex-col items-center gap-1">
        <Clock />
        <Quote />
      </div>
      <SearchBox />
    </BottomCenter>

    <RightTop></RightTop>
  </div>

  <div id="sh-background" class="fixed top-0 left-0 -z-1 h-screen w-screen">
    <img
      src="@assets/bg-images/background.png"
      alt="Background"
      class="h-full w-full object-cover opacity-70"
    />
  </div>
</template>
