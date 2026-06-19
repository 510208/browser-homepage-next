<script setup lang="ts">
import Clock from "@/components/home/Clock.vue";
import SearchBox from "@/components/home/SearchBox.vue";

import BottomCenter from "./components/container/BottomCenter.vue";
</script>

<template>
  <div id="sh-main" class="h-screen w-screen bg-transparent">
    <BottomCenter>
      <Clock />
      <SearchBox />
    </BottomCenter>
  </div>

  <div id="sh-background" class="fixed top-0 left-0 -z-1 h-screen w-screen">
    <img
      src="@assets/bg-images/background.png"
      alt="Background"
      class="h-full w-full object-cover opacity-70"
    />
  </div>
</template>
