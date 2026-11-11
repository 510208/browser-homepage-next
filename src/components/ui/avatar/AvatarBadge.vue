<!-- bg-green-800 -->
<template>
  <div
    class="absolute size-3 border-1 right-0 bottom-0 rounded-full"
    :class="class"
  />
</template>

<script setup lang="ts">
import type { HTMLAttributes } from "vue";

const props = defineProps<{ class?: HTMLAttributes["class"] }>();
</script>
