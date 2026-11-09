<script setup lang="ts">
import type { UptimeStatus } from "@/lib/uptime-kuma/utils";
import { formatUptime, statusColors } from "@/lib/uptime-kuma/utils";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

defineProps<{ uptime: number | null; status: UptimeStatus; badge?: boolean }>();
</script>

<template>
  <Tooltip>
    <TooltipTrigger as-child>
      <Badge
        :aria-label="`過去 24 小時${badge ? '群組平均' : ''}可用率：${formatUptime(uptime)}`"
        :class="
          badge
            ? 'min-w-[50px] px-1.5 text-base leading-[1.1] font-normal'
            : 'w-full justify-end rounded-none border-0 bg-transparent p-0 text-sm leading-[1.1] font-normal'
        "
        :style="
          badge
            ? {
                backgroundColor: statusColors[status].color,
                color: statusColors[status].foreground,
                borderColor: statusColors[status].foreground,
              }
            : { color: statusColors[status].color }
        "
      >
        {{ formatUptime(uptime) }}
      </Badge>
    </TooltipTrigger>
    <TooltipContent
      >過去 24 小時{{ badge ? "群組平均" : "" }}可用率：{{ formatUptime(uptime) }}</TooltipContent
    >
  </Tooltip>
</template>
