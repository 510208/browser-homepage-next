<script setup lang="ts">
import type { UptimeStatus } from "@/lib/uptime-kuma/utils";
import { Circle } from "@lucide/vue";
import { statusColors } from "@/lib/uptime-kuma/utils";

defineProps<{ status: UptimeStatus; large?: boolean; group?: boolean }>();
</script>

<template>
  <Circle
    aria-hidden="true"
    class="shrink-0 fill-current transition-colors duration-200 motion-reduce:transition-none"
    :class="large ? 'size-[18px]' : 'size-2'"
    :stroke-width="0"
    :style="{
      color:
        large && status === 'up'
          ? 'rgba(205, 244, 205, 0.9)'
          : group && status === 'maintenance'
            ? '#7782c9'
            : statusColors[status].color,
    }"
  />
</template>
