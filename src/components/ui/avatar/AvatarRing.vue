<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { inject, onBeforeUnmount } from "vue";
import { cn } from "@/lib/utils";
import { avatarRingKey } from "./avatar-context";

const props = defineProps<{
  class?: HTMLAttributes["class"];
}>();

const ringCount = inject(avatarRingKey);

if (ringCount) {
  ringCount.value++;
}

onBeforeUnmount(() => {
  if (ringCount) {
    ringCount.value--;
  }
});
</script>

<template>
  <div
    data-slot="avatar-ring"
    aria-hidden="true"
    :class="
      cn('pointer-events-none absolute inset-0 z-0 rounded-full', props.class)
    "
  />
</template>
