<script setup lang="ts">
import { computed } from "vue";
import type { UptimeKumaHeartbeat } from "@/types/uptimeKuma";
import { heartbeatSegments, statusColors, statusLabels } from "@/lib/uptime-kuma/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

const props = defineProps<{ heartbeats: UptimeKumaHeartbeat[] }>();
const segments = computed(() => heartbeatSegments(props.heartbeats));
const description = computed(
  () =>
    `最近心跳紀錄，由舊到新：${segments.value.map((segment) => statusLabels[segment.status]).join("、")}`,
);
</script>

<template>
  <span
    role="img"
    :aria-label="description"
    class="flex h-7 min-w-0 gap-px overflow-hidden rounded"
  >
    <Tooltip v-for="(segment, index) in segments" :key="index">
      <TooltipTrigger as-child>
        <span
          class="h-full min-w-0 flex-1 transition-opacity duration-150 hover:opacity-75 motion-reduce:transition-none"
          :style="{
            backgroundColor:
              segment.status === 'maintenance' ? '#7782c9' : statusColors[segment.status].color,
          }"
        />
      </TooltipTrigger>
      <TooltipContent class="max-w-64">{{ segment.label }}</TooltipContent>
    </Tooltip>
  </span>
</template>
