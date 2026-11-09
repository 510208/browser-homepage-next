<script setup lang="ts">
import { computed } from "vue";
import type { UptimeKumaHeartbeat } from "@/types/uptimeKuma";
import type { UptimeStatus } from "@/lib/uptime-kuma/utils";
import { pingSegments, sortedHeartbeats, statusColors } from "@/lib/uptime-kuma/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

const props = defineProps<{ heartbeats: UptimeKumaHeartbeat[]; status: UptimeStatus }>();
const segments = computed(() => pingSegments(props.heartbeats));
const description = computed(() => {
  const ping = sortedHeartbeats(props.heartbeats).at(-1)?.ping;
  return `最近 18 次回應時間，最新：${typeof ping === "number" && Number.isFinite(ping) && ping >= 0 ? `${ping} ms` : "無資料"}`;
});
</script>

<template>
  <Tooltip>
    <TooltipTrigger as-child>
      <svg
        v-if="segments.length"
        viewBox="0 0 108 16"
        width="108"
        height="16"
        role="img"
        :aria-label="description"
        class="h-4 w-full"
        :style="{ color: statusColors[status].color }"
      >
        <title>{{ description }}</title>
        <template v-for="(points, index) in segments" :key="index">
          <polyline
            v-if="points.includes(' ')"
            :points="points"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <circle
            v-else
            :cx="points.split(',')[0]"
            :cy="points.split(',')[1]"
            r="1"
            fill="currentColor"
          />
        </template>
      </svg>
      <span v-else class="text-center text-xs text-brown-500" aria-label="尚無回應時間資料">—</span>
    </TooltipTrigger>
    <TooltipContent>{{ description }}</TooltipContent>
  </Tooltip>
</template>
