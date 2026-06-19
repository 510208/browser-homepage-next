<script setup lang="ts">
import { Clock } from "@/components/widgets/clock";
import { SearchBox } from "@/components/widgets/search-box";
import { Quote } from "@/components/widgets/quote";
import { Avatar } from "@/components/widgets/avatar";

import BottomCenter from "@/components/container/BottomCenter.vue";
import RightTop from "@/components/container/RightTop.vue";
import Bookmarks from "@/components/widgets/bookmarks/Bookmarks.vue";
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
    </RightTop>

    <Bookmarks />
  </div>

  <div id="sh-background" class="fixed top-0 left-0 -z-10 h-screen w-screen">
    <img
      src="@assets/bg-images/background.png"
      alt="Background"
      class="h-full w-full object-cover opacity-70"
    />
  </div>
</template>
