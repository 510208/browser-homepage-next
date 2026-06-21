<template>
  <div :class="cn('relative overflow-hidden p-2.5', props.class)">
    <!-- 圖示 -->
    <div class="absolute right-0 -bottom-[13px] z-0">
      <slot name="icon" />
    </div>

    <!-- 內容 -->
    <div class="z-10 flex flex-col gap-0.5">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { cn } from "@/lib/utils";

const props = defineProps<{
  class?: string;
}>();
</script>