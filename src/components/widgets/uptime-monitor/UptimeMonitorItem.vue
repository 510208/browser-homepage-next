<script setup lang="ts">
import type { UptimeMonitorData } from "@/lib/uptime-kuma/utils";
import { statusLabels } from "@/lib/uptime-kuma/utils";
import { Minus } from "@lucide/vue";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import UptimeStatusDot from "./UptimeStatusDot.vue";
import UptimePingChart from "./UptimePingChart.vue";
import UptimeRate from "./UptimeRate.vue";

defineProps<{ monitor: UptimeMonitorData }>();
</script>

<template>
  <li
    class="grid grid-cols-[minmax(0,120px)_minmax(0,1fr)_44px] items-center gap-2 text-sm leading-[1.1]"
  >
    <Tooltip>
      <TooltipTrigger as-child>
        <span class="flex min-w-0 items-center gap-1">
          <Minus aria-hidden="true" class="h-2 w-3.5 shrink-0 text-brown-600" :stroke-width="1" />
          <UptimeStatusDot :status="monitor.status" />
          <span class="truncate text-brown-300">{{ monitor.name }}</span>
          <span class="sr-only">：{{ statusLabels[monitor.status] }}</span>
        </span>
      </TooltipTrigger>
      <TooltipContent>{{ monitor.name }}：{{ statusLabels[monitor.status] }}</TooltipContent>
    </Tooltip>
    <UptimePingChart :heartbeats="monitor.heartbeats" :status="monitor.status" />
    <UptimeRate :uptime="monitor.uptime" :status="monitor.status" />
  </li>
</template>
